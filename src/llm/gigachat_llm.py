"""Gigachat (Sber) LLM Integration (Demo Example)"""
import requests

class GigachatLLM:
    def __init__(self, api_endpoint: str, api_key: str):
        self.api_endpoint = api_endpoint
        self.api_key = api_key

    def generate_answer(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {"prompt": prompt, "max_tokens": 200}
            resp = requests.post(self.api_endpoint, json=data, headers=headers, timeout=30)
            resp.raise_for_status()
            answer = resp.json().get("answer", "")
            return answer
        except Exception as e:
            return f"[Gigachat Error]: {str(e)}"
