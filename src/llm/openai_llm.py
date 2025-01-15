"""OpenAI LLM Integration"""
import os
import openai

class OpenAILLM:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_answer(self, prompt: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[OpenAI Error]: {str(e)}"
