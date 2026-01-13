from threading import Thread
from typing import Generator, List, Dict, Union

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
)


class LLM:
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

    # -------------------------
    # NON-STREAM GENERATION
    # -------------------------
    def generate(self, prompt: str) -> str:
        # Enforce plain text prompting (LOCKED)
        text = f"You are a helpful coding assistant.\n\nUser: {prompt}\nAssistant:\n"

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
        # Enforce plain text prompting (LOCKED)
        text = f"You are a helpful coding assistant.\n\nUser: {prompt}\nAssistant:\n"

        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        streamer = TextIteratorStreamer(
            self.tokenizer,
            skip_prompt=True,         # LOCKED
            skip_special_tokens=True, # LOCKED
        )

        generation_kwargs = dict(
            **inputs,
            streamer=streamer,
            max_new_tokens=400,      # LOCKED
            do_sample=False,         # LOCKED
            use_cache=True,          # LOCKED
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
        )

        thread = Thread(
            target=self.model.generate,
            kwargs=generation_kwargs,
            daemon=True,
        )
        thread.start()

        for chunk in streamer:
            if chunk:
                yield chunk
