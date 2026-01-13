from threading import Thread, Lock, Event
from typing import Generator, List, Dict, Union, Optional
import time

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
        self.model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="auto",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            trust_remote_code=True,
        )

        self.model.eval()
    
    @classmethod
    def cancel_current_generation(cls):
        """Cancel any ongoing generation."""
        print("[DEBUG] cancel_current_generation called")
        if cls._cancel_event:
            print("[DEBUG] Setting cancel event")
            cls._cancel_event.set()
        else:
            print("[DEBUG] No cancel event found")
            
        if cls._current_thread and cls._current_thread.is_alive():
            print(f"[DEBUG] Waiting for current thread {cls._current_thread.name} to join...")
            # Give it a moment to stop
            cls._current_thread.join(timeout=2)
            if cls._current_thread.is_alive():
                print("[DEBUG] Thread did NOT join in time!")
            else:
                print("[DEBUG] Thread joined successfully")
        else:
            print("[DEBUG] No active thread to join")
            
        cls._current_thread = None
        cls._cancel_event = None
        print("[DEBUG] Cancel complete")

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
                    # No StoppingCriteria needed for non-streaming as we wait for it synchronously
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
        print("[DEBUG] stream_generate: starting")
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

        print("[DEBUG] Starting generation thread")
        thread = Thread(
            target=self.model.generate,
            kwargs=generation_kwargs,
            daemon=True,
        )
        LLM._current_thread = thread
        thread.start()

        # Yield chunks while thread is running
        try:
            print("[DEBUG] Yielding chunks...")
            for chunk in streamer:
                # Check if cancelled
                if cancel_event.is_set():
                    print("[DEBUG] Streamer loop cancelled by event")
                    break
                if chunk:
                    yield chunk
            print("[DEBUG] Streamer loop finished")
        except Exception as e:
            print(f"[DEBUG] Streamer loop error: {e}")
        finally:
            print("[DEBUG] Streamer finally block")
            # Signal cancellation just in case loop exited otherwise
            cancel_event.set()
            # Wait for thread to complete (but don't block forever if getting garbage collected)
            # using a short timeout here is safer for finally block
            print("[DEBUG] Joining thread...")
            thread.join(timeout=2)
            if thread.is_alive():
                print("[DEBUG] Thread failed to join in finally block")
            else:
                print("[DEBUG] Thread joined in finally block")
                
            # Cleanup if this is still the active thread
            if LLM._current_thread == thread:
                LLM._current_thread = None
                LLM._cancel_event = None



