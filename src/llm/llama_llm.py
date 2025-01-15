"""Llama LLM Integration via Hugging Face"""
import os
from huggingface_hub import hf_hub_download
from transformers import LlamaTokenizer, LlamaForCausalLM
import torch

class LlamaLLM:
    def __init__(self, hf_model_id: str = 'decapoda-research/llama-7b-hf', download: bool = True, local_path: str = None, hf_token: str = None):
        self.hf_model_id = hf_model_id
        self.download = download
        self.local_path = local_path
        self.hf_token = hf_token

        if download and not local_path:
            download_dir = "./models/llama"
            os.makedirs(download_dir, exist_ok=True)
            # Демонстрационно скачиваем, фактически нужно скачать config, tokenizer, weights и т.д.
            self.tokenizer = LlamaTokenizer.from_pretrained(self.hf_model_id, use_auth_token=self.hf_token, cache_dir=download_dir)
            self.model = LlamaForCausalLM.from_pretrained(self.hf_model_id, use_auth_token=self.hf_token, cache_dir=download_dir)
        else:
            # Загружаем локально
            self.tokenizer = LlamaTokenizer.from_pretrained(local_path)
            self.model = LlamaForCausalLM.from_pretrained(local_path)

        self.model.eval()
        if torch.cuda.is_available():
            self.model.to("cuda")

    def generate_answer(self, prompt: str) -> str:
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_new_tokens=128, do_sample=True, top_k=50)
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return answer
        except Exception as e:
            return f"[Llama Error]: {str(e)}"
