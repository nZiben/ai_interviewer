"""LLM evaluation utilities for scoring and feedback"""

def get_llm_feedback(question: str, answer: str, llm) -> str:
    """Get feedback from LLM"""
    try:
        prompt = f"""Оцени ответ на вопрос интервью и дай краткую обратную связь.
        Вопрос: {question}
        Ответ: {answer}
        
        Формат ответа: только обратная связь, без оценки."""
        
        feedback = llm.generate_answer(prompt)
        return feedback.strip()
    except Exception as e:
        return "Не удалось получить обратную связь"

def get_llm_score(question: str, answer: str, llm) -> int:
    """Get score from LLM"""
    try:
        prompt = f"""Оцени ответ на вопрос интервью по шкале от 1 до 5.
        Вопрос: {question}
        Ответ: {answer}
        
        Формат ответа: только число от 1 до 5."""
        
        score_text = llm.generate_answer(prompt)
        try:
            score = int(score_text.strip())
            return max(1, min(5, score))  # Ограничиваем оценку от 1 до 5
        except ValueError:
            return 3  # Возвращаем среднюю оценку в случае ошибки
    except Exception as e:
        return 3  # Возвращаем среднюю оценку в случае ошибки 