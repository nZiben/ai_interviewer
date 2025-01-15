"""Mistral LLM Integration (Demo via Hugging Face)"""
import os
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class MistralLLM:
    def __init__(self, hf_model_id: str, hf_token: str = None, local_path: str = None):
        """
        :param hf_model_id: e.g. 'mistralai/Mistral-7B-v0.1'
        :param hf_token: Optional Hugging Face token for private models
        :param local_path: Local path to model (if already downloaded)
        """
        self.hf_model_id = hf_model_id
        self.hf_token = hf_token
        self.local_path = local_path

        if not local_path:
            # Скачиваем модель в папку ./models/mistral
            download_dir = "./models/mistral"
            os.makedirs(download_dir, exist_ok=True)
            # По умолчанию скачиваем бинарно из hf_hub_download
            self.tokenizer_path = hf_hub_download(repo_id=hf_model_id, filename='tokenizer.model', token=hf_token, cache_dir=download_dir)
            self.model_path = hf_hub_download(repo_id=hf_model_id, filename='pytorch_model.bin', token=hf_token, cache_dir=download_dir)
            # Фактически для полноценных моделей обычно нужно скачивать config, merges и т.п.
            self.tokenizer = AutoTokenizer.from_pretrained(hf_model_id, use_auth_token=hf_token, cache_dir=download_dir)
            self.model = AutoModelForCausalLM.from_pretrained(hf_model_id, use_auth_token=hf_token, cache_dir=download_dir)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(local_path)
            self.model = AutoModelForCausalLM.from_pretrained(local_path)

        self.model.eval()
        if torch.cuda.is_available():
            self.model.to("cuda")

    def generate_answer(self, prompt: str) -> str:
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k,v in inputs.items()}
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_new_tokens=128, do_sample=True, top_k=50)
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return answer
        except Exception as e:
            return f"[Mistral Error]: {str(e)}"
