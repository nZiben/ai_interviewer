"""Utility for Prompt Generation"""

class PromptGenerator:
    @staticmethod
    def generate_prompt(question: str) -> str:
        return f"Please analyze the following question and provide an answer: {question}"
