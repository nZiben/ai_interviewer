import os
from mistralai import Mistral

class MistralAPILLM:
    def __init__(self, api_key: str = None, model: str = "mistral-large-latest"):
        if api_key is None:
            api_key = os.environ["MISTRAL_API_KEY"]

        self.api_key = api_key
        self.model = model
        self.client = Mistral(api_key=self.api_key)

    def generate_answer(self, prompt: str) -> str:
        try:
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
            response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Mistral API Error]: {str(e)}"