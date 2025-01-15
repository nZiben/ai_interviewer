import unittest
from src.llm.openai_llm import OpenAILLM

class TestLLM(unittest.TestCase):
    def test_openai_generate_answer(self):
        llm = OpenAILLM(api_key="fake_key")
        response = llm.generate_answer("Hello")
        self.assertIn("[OpenAI Error]", response, "Should fail with fake key")

if __name__ == '__main__':
    unittest.main()
