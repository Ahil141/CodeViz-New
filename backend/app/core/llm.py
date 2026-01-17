from threading import Thread, Lock, Event
from typing import Generator, List, Dict, Union, Optional
import time
import sys

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
    StoppingCriteria,
    StoppingCriteriaList,
)


class CancellationCriteria(StoppingCriteria):
    def __init__(self, cancel_event: Event):
        self.cancel_event = cancel_event

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        return self.cancel_event.is_set()


class LLM:
    # Class-level lock to prevent concurrent generations
    _generation_lock = Lock()
    _current_thread: Optional[Thread] = None
    _cancel_event: Optional[Event] = None
    
    def __init__(self):
        print("\n[LLM INIT] Initializing Model Loading Process...")
        
        # ---------------------------------------------------------
        # GPU CHECK - Ensure we are actually using the RTX 3050
        # ---------------------------------------------------------
        if not torch.cuda.is_available():
            print("[WARNING] CUDA/GPU is NOT available. Running on CPU will be slow.")
            self.device_type = "cpu"
        else:
            gpu_name = torch.cuda.get_device_name(0)
            print(f"[SUCCESS] CUDA/GPU detected: {gpu_name}")
            print(f"[INFO] VRAM Available: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
            self.device_type = "cuda"

        self.model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

        print(f"[LLM INIT] Loading Tokenizer: {self.model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )

        print(f"[LLM INIT] Loading Model to {self.device_type}...")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="cuda",  # <--- FORCES GPU OR CRASHES
            torch_dtype=torch.float16 if self.device_type == "cuda" else torch.float32,
            trust_remote_code=True,
        )

        self.model.eval()
        print(f"[LLM INIT] Model loaded successfully on device: {self.model.device}")
        print("---------------------------------------------------------")
    
    @classmethod
    def cancel_current_generation(cls):
        """Cancel any ongoing generation."""
        # print("[DEBUG] cancel_current_generation called")
        if cls._cancel_event:
            # print("[DEBUG] Setting cancel event")
            cls._cancel_event.set()
        
        if cls._current_thread and cls._current_thread.is_alive():
            print(f"[DEBUG] Waiting for current thread {cls._current_thread.name} to join...")
            cls._current_thread.join(timeout=2)
            
        cls._current_thread = None
        cls._cancel_event = None

    # -------------------------
    # NON-STREAM GENERATION
    # -------------------------
    def generate(self, prompt: str) -> str:
        # Cancel any previous generation first
        LLM.cancel_current_generation()
        
        # Enforce plain text prompting (LOCKED)
        text = f"You are a helpful coding assistant.\n\nUser: {prompt}\nAssistant:\n"

        with LLM._generation_lock:
            inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)
            input_len = inputs.input_ids.shape[-1]

            with torch.no_grad():
                output = self.model.generate(
                    **inputs,
                    max_new_tokens=400,  # LOCKED
                    do_sample=False,     # LOCKED
                    use_cache=True,      # LOCKED
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )

            generated = output[0][input_len:]
            return self.tokenizer.decode(
                generated,
                skip_special_tokens=True,
            ).strip()

    # -------------------------
    # STREAMING GENERATION
    # -------------------------
    def stream_generate(
        self,
        prompt: str,
    ) -> Generator[str, None, None]:
        # Cancel any previous generation first
        LLM.cancel_current_generation()
        
        # Create new cancel event for this generation
        LLM._cancel_event = Event()
        cancel_event = LLM._cancel_event
        
        # Enforce plain text prompting (LOCKED)
        text = f"You are a helpful coding assistant.\n\nUser: {prompt}\nAssistant:\n"

        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        streamer = TextIteratorStreamer(
            self.tokenizer,
            skip_prompt=True,         # LOCKED
            skip_special_tokens=True, # LOCKED
        )
        
        stopping_criteria = StoppingCriteriaList([CancellationCriteria(cancel_event)])

        generation_kwargs = dict(
            **inputs,
            streamer=streamer,
            max_new_tokens=400,      # LOCKED
            do_sample=False,         # LOCKED
            use_cache=True,          # LOCKED
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            stopping_criteria=stopping_criteria,
        )

        thread = Thread(
            target=self.model.generate,
            kwargs=generation_kwargs,
            daemon=True,
        )
        LLM._current_thread = thread
        thread.start()

        # Yield chunks while thread is running
        try:
            for chunk in streamer:
                # Check if cancelled
                if cancel_event.is_set():
                    break
                if chunk:
                    yield chunk
        except Exception as e:
            print(f"[DEBUG] Streamer loop error: {e}")
        finally:
            # Signal cancellation just in case loop exited otherwise
            cancel_event.set()
            # Wait for thread to complete
            thread.join(timeout=2)
                
            # Cleanup if this is still the active thread
            if LLM._current_thread == thread:
                LLM._current_thread = None
                LLM._cancel_event = None