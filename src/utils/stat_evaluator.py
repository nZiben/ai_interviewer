"""Statistical Evaluator for Survey Results"""
import numpy as np
import pandas as pd
from scipy import stats
from typing import List, Tuple, Dict

class StatEvaluator:
    def __init__(self):
        self.min_samples = 8  # Минимальное количество образцов для статистических тестов
    
    def _select_test(self, llm_scores: List[float], human_scores: List[float]) -> str:
        """Выбирает подходящий статистический тест на основе данных"""
        if len(llm_scores) < self.min_samples or len(human_scores) < self.min_samples:
            return "descriptive"  # Для малых выборок используем только описательную статистику
            
        # Проверяем нормальность распределения
        _, llm_p = stats.normaltest(llm_scores)
        _, human_p = stats.normaltest(human_scores)
        
        # Если оба распределения нормальные, используем t-тест
        if llm_p > 0.05 and human_p > 0.05:
            return "t-test"
        # Если хотя бы одно распределение не нормальное, используем тест Манна-Уитни
        else:
            return "mann-whitney"
    
    def _perform_test(self, test_type: str, llm_scores: List[float], human_scores: List[float]) -> Tuple[float, float]:
        """Выполняет выбранный статистический тест"""
        if test_type == "descriptive":
            return 0.0, 1.0  # Для малых выборок возвращаем p-value = 1.0
        elif test_type == "t-test":
            return stats.ttest_ind(llm_scores, human_scores)
        else:  # mann-whitney
            return stats.mannwhitneyu(llm_scores, human_scores, alternative='two-sided')
    
    def _get_conclusion(self, test_type: str, p_value: float, llm_mean: float, human_mean: float) -> str:
        """Формирует вывод на основе результатов теста"""
        if test_type == "descriptive":
            return "Недостаточно данных для статистического анализа"
            
        if p_value < 0.05:
            if llm_mean > human_mean:
                return "Есть статистически значимые различия: LLM оценивает выше"
            else:
                return "Есть статистически значимые различия: человек оценивает выше"
        else:
            return "Нет статистически значимых различий между оценками"
    
    def evaluate_scores(self, llm_scores: List[float], human_scores: List[float]) -> pd.DataFrame:
        """Оценивает различия между оценками LLM и человека"""
        # Преобразуем списки в numpy массивы
        llm_scores = np.array(llm_scores)
        human_scores = np.array(human_scores)
        
        # Выбираем тест
        test_type = self._select_test(llm_scores, human_scores)
        
        # Вычисляем описательную статистику
        llm_mean = np.mean(llm_scores)
        human_mean = np.mean(human_scores)
        llm_std = np.std(llm_scores)
        human_std = np.std(human_scores)
        
        # Выполняем тест
        if test_type != "descriptive":
            test_stat, p_value = self._perform_test(test_type, llm_scores, human_scores)
        else:
            test_stat, p_value = 0.0, 1.0
        
        # Формируем вывод
        conclusion = self._get_conclusion(test_type, p_value, llm_mean, human_mean)
        
        # Создаем DataFrame с результатами
        results = {
            'Метрика': [
                'Тест',
                'Среднее LLM',
                'Среднее человек',
                'Стд. откл. LLM',
                'Стд. откл. человек',
                'Статистика теста',
                'p-value',
                'Вывод'
            ],
            'Значение': [
                test_type,
                f"{llm_mean:.2f}",
                f"{human_mean:.2f}",
                f"{llm_std:.2f}",
                f"{human_std:.2f}",
                f"{test_stat:.2f}" if test_type != "descriptive" else "N/A",
                f"{p_value:.4f}" if test_type != "descriptive" else "N/A",
                conclusion
            ]
        }
        
        return pd.DataFrame(results) 