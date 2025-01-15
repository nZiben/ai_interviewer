"""Claude LLM Integration"""
import os
import anthropic

class ClaudeLLM:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = anthropic.Client(api_key)

    def generate_answer(self, prompt: str) -> str:
        try:
            resp = self.client.completion(
                prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
                stop_sequences=[anthropic.HUMAN_PROMPT],
                model="claude-2",
                max_tokens_to_sample=256
            )
            return resp["completion"]
        except Exception as e:
            return f"[Claude Error]: {str(e)}"
