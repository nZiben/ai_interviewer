"""Streamlit Admin Interface for Survey"""
import streamlit as st
import os
import sys
import pandas as pd
from pathlib import Path
from src.database.db_handler import DBHandler
from src.llm.mistral_api_llm import MistralAPILLM
from src.utils.question_manager import QuestionManager
from src.utils.stat_evaluator import StatEvaluator
from src.database.models import Test, Question, SurveyResult
from datetime import datetime, timedelta
import plotly.express as px

# Добавляем корневую директорию проекта в PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Инициализация базы данных и менеджера вопросов
db_handler = DBHandler()
question_manager = QuestionManager(db_handler)
stat_evaluator = StatEvaluator()

def check_password():
    """Проверяет пароль администратора."""
    def password_entered():
        if st.session_state["password"] == os.getenv("ADMIN_PASSWORD", "admin"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.text_input("Пароль", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Пароль", type="password", on_change=password_entered, key="password")
        st.error("Неверный пароль")
        return False
    else:
        return True

def admin_app():
    if not check_password():
        st.stop()
    st.title("Панель администратора")
    
    # Создаем вкладки
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Просмотр ответов", 
        "Оценка ответов", 
        "Статистика", 
        "Управление вопросами",
        "Настройка моделей"
    ])
    
    # Вкладка "Просмотр ответов"
    with tab1:
        st.header("Просмотр ответов")
        
        # Получаем список всех тестов
        tests = question_manager.get_all_tests()
        if not tests:
            st.warning("Нет доступных тестов")
            return
        
        # Выбор теста для просмотра
        selected_test = st.selectbox("Выберите тест", tests)
        
        # Получаем результаты для выбранного теста
        session = db_handler.get_session()
        try:
            # Добавляем отладочную информацию
            st.write(f"Выбранный тест: {selected_test}")
            
            # Получаем все результаты
            all_results = session.query(SurveyResult).all()
            st.write(f"Всего результатов в базе: {len(all_results)}")
            
            # Фильтруем результаты по выбранному тесту
            results = [r for r in all_results if r.test_name == selected_test]
            st.write(f"Результатов для выбранного теста: {len(results)}")
            
            if not results:
                st.info("Нет результатов для выбранного теста")
                return
            
            # Преобразуем результаты в DataFrame
            results_data = []
            for result in results:
                results_data.append({
                    'Имя': result.first_name,
                    'Фамилия': result.last_name,
                    'Вопрос': result.question,
                    'Ответ': result.answer,
                    'Оценка LLM': result.llm_score,
                    'Обратная связь': result.feedback,
                    'Дата': result.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            df = pd.DataFrame(results_data)
            
            # Отображаем результаты в виде таблицы
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            
            # Добавляем возможность скачать результаты в CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Скачать результаты",
                csv,
                f"results_{selected_test}.csv",
                "text/csv",
                key='download-csv'
            )
            
        finally:
            session.close()
    
    # Вкладка "Оценка ответов"
    with tab2:
        st.header("Оценка ответов")
        
        # Получаем список всех тестов
        tests = question_manager.get_all_tests()
        if not tests:
            st.warning("Нет доступных тестов")
            return
        
        # Выбор теста для оценки
        selected_test = st.selectbox("Выберите тест для оценки", tests, key="evaluation_test")
        
        # Получаем результаты для выбранного теста
        session = db_handler.get_session()
        try:
            results = session.query(SurveyResult).filter_by(test_name=selected_test).all()
            
            if not results:
                st.info("Нет результатов для оценки")
                return
            
            # Группируем результаты по пользователям
            user_results = {}
            for result in results:
                key = f"{result.first_name} {result.last_name}"
                if key not in user_results:
                    user_results[key] = []
                user_results[key].append(result)
            
            # Отображаем результаты для оценки
            for user, user_data in user_results.items():
                with st.expander(f"Результаты пользователя: {user}"):
                    for result in user_data:
                        st.write(f"**Вопрос:** {result.question}")
                        st.write(f"**Ответ:** {result.answer}")
                        st.write(f"**Оценка LLM:** {result.llm_score}/5")
                        st.write(f"**Обратная связь LLM:** {result.feedback}")
                        
                        # Поле для ввода оценки
                        human_score = st.number_input(
                            "Ваша оценка (1-5)",
                            min_value=1,
                            max_value=5,
                            value=int(result.llm_score) if result.llm_score else 3,
                            key=f"score_{result.id}"
                        )
                        
                        if st.button("Сохранить оценку", key=f"save_{result.id}"):
                            # Создаем новую сессию для обновления
                            update_session = db_handler.get_session()
                            try:
                                # Получаем свежую копию результата
                                result_to_update = update_session.query(SurveyResult).get(result.id)
                                if result_to_update:
                                    result_to_update.score = human_score
                                    update_session.commit()
                                    st.success("Оценка сохранена")
                                    st.rerun()  # Перезагружаем страницу для обновления данных
                                else:
                                    st.error("Результат не найден")
                            except Exception as e:
                                update_session.rollback()
                                st.error(f"Ошибка при сохранении оценки: {str(e)}")
                            finally:
                                update_session.close()
                        
                        st.write("---")
        
        finally:
            session.close()
    
    # Вкладка "Статистика"
    with tab3:
        st.header("Статистика")
        
        # Получаем список всех тестов
        tests = question_manager.get_all_tests()
        if not tests:
            st.warning("Нет доступных тестов")
            return
        
        # Выбор теста для просмотра статистики
        selected_test = st.selectbox("Выберите тест", tests, key="stats_test")
        
        # Выбор периода
        period = st.selectbox(
            "Выберите период",
            ["Все время", "Последние 7 дней", "Последние 30 дней"]
        )
        
        # Получаем результаты для выбранного теста
        session = db_handler.get_session()
        try:
            query = session.query(SurveyResult).filter_by(test_name=selected_test)
            
            # Фильтруем по периоду
            if period == "Последние 7 дней":
                query = query.filter(SurveyResult.timestamp >= datetime.now() - timedelta(days=7))
            elif period == "Последние 30 дней":
                query = query.filter(SurveyResult.timestamp >= datetime.now() - timedelta(days=30))
            
            results = query.all()
            
            if not results:
                st.info("Нет данных для отображения статистики")
                return
            
            # Собираем оценки LLM и человека
            llm_scores = []
            human_scores = []
            for result in results:
                if result.llm_score is not None:
                    llm_scores.append(result.llm_score)
                if result.score is not None:
                    human_scores.append(result.score)
            
            # Рассчитываем статистику с помощью StatEvaluator
            stats_df = stat_evaluator.evaluate_scores(llm_scores, human_scores)
            
            # Отображаем результаты статистического анализа
            st.subheader("Статистический анализ оценок")
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
            
            # Дополнительная статистика
            st.subheader("Дополнительная статистика")
            
            # Общая статистика
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Всего ответов", len(results))
            with col2:
                st.metric("Оценено человеком", len(human_scores))
            
            # Распределение оценок
            st.subheader("Распределение оценок")
            
            # Создаем DataFrame для графика
            score_data = pd.DataFrame({
                'Оценка': list(range(1, 6)) * 2,
                'Тип': ['LLM'] * 5 + ['Человек'] * 5,
                'Количество': [llm_scores.count(i) for i in range(1, 6)] + [human_scores.count(i) for i in range(1, 6)]
            })
            
            # Группированная гистограмма с помощью plotly
            fig = px.bar(
                score_data,
                x='Оценка',
                y='Количество',
                color='Тип',
                barmode='group',
                text_auto=True,
                labels={'Оценка': 'Оценка', 'Количество': 'Количество', 'Тип': 'Тип'}
            )
            fig.update_layout(
                xaxis=dict(dtick=1),
                bargap=0.2,
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Статистика по вопросам
            st.subheader("Статистика по вопросам")
            
            # Группируем результаты по вопросам
            question_stats = {}
            for result in results:
                if result.question not in question_stats:
                    question_stats[result.question] = {
                        'llm_scores': [],
                        'human_scores': []
                    }
                if result.llm_score is not None:
                    question_stats[result.question]['llm_scores'].append(result.llm_score)
                if result.score is not None:
                    question_stats[result.question]['human_scores'].append(result.score)
            
            # Отображаем статистику по каждому вопросу
            for question, stats in question_stats.items():
                with st.expander(f"Вопрос: {question}"):
                    # Рассчитываем статистику для вопроса
                    question_df = stat_evaluator.evaluate_scores(
                        stats['llm_scores'],
                        stats['human_scores']
                    )
                    st.dataframe(question_df, use_container_width=True, hide_index=True)
        
        finally:
            session.close()
    
    # Вкладка "Управление вопросами"
    with tab4:
        st.header("Управление вопросами")
        
        # Создание нового теста
        st.subheader("Создание теста")
        new_test_name = st.text_input("Название нового теста")
        if st.button("Создать тест"):
            if new_test_name:
                if question_manager.create_test(new_test_name):
                    st.success(f"Тест '{new_test_name}' успешно создан")
                    st.rerun()
                else:
                    st.error("Тест с таким названием уже существует")
            else:
                st.warning("Введите название теста")
        
        # Выбор теста для управления вопросами
        available_tests = question_manager.get_all_tests()
        if not available_tests:
            st.warning("Нет доступных тестов")
            return
        
        selected_test = st.selectbox("Выберите тест для управления вопросами", available_tests)
        
        # Добавление вопросов
        st.subheader("Добавление вопросов")
        new_questions = st.text_area(
            "Введите вопросы (каждый вопрос с новой строки)",
            help="Введите несколько вопросов, разделяя их переносами строк"
        )
        if st.button("Добавить вопросы"):
            if new_questions:
                questions = [q.strip() for q in new_questions.split('\n') if q.strip()]
                success_count = 0
                for question in questions:
                    if question_manager.add_question_to_test(selected_test, question):
                        success_count += 1
                st.success(f"Успешно добавлено {success_count} вопросов")
                st.rerun()
            else:
                st.warning("Введите хотя бы один вопрос")
        
        # Генерация вопросов с помощью LLM
        st.subheader("Генерация вопросов")
        topic = st.text_input("Введите тему для генерации вопросов")
        num_questions = st.number_input("Количество вопросов", min_value=1, max_value=10, value=3)
        
        if st.button("Сгенерировать вопросы"):
            if topic:
                with st.spinner("Генерация вопросов..."):
                    # Генерация вопросов с помощью LLM
                    llm = MistralAPILLM()
                    prompt = f"""Сгенерируй {num_questions} открытых вопросов для интервью по теме: {topic}
                    Вопросы должны быть:
                    - Открытыми (требующими развернутого ответа)
                    - Релевантными теме
                    - Профессиональными
                    
                    Формат: каждый вопрос с новой строки, без нумерации"""
                    
                    response = llm.generate_answer(prompt)
                    questions = [q.strip() for q in response.split('\n') if q.strip()]
                    
                    # Сохраняем сгенерированные вопросы
                    if 'generated_questions' not in st.session_state:
                        st.session_state.generated_questions = []
                    st.session_state.generated_questions = questions
                    
                    st.success("Вопросы сгенерированы!")
            else:
                st.warning("Введите тему для генерации вопросов")
        
        # Отображение сгенерированных вопросов
        if 'generated_questions' in st.session_state and st.session_state.generated_questions:
            st.write("Сгенерированные вопросы:")
            for i, question in enumerate(st.session_state.generated_questions, 1):
                st.write(f"{i}. {question}")
            
            if st.button("Добавить все вопросы в тест"):
                success_count = 0
                for question in st.session_state.generated_questions:
                    if question_manager.add_question_to_test(selected_test, question):
                        success_count += 1
                st.success(f"Успешно добавлено {success_count} вопросов")
                st.session_state.generated_questions = []
                st.rerun()
        
        # Просмотр и редактирование существующих вопросов
        st.subheader("Существующие вопросы")
        questions = question_manager.get_questions_for_test(selected_test)
        if questions:
            for i, question in enumerate(questions, 1):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"{i}. {question}")
                with col2:
                    if st.button("Удалить", key=f"del_{i}"):
                        if question_manager.delete_question(selected_test, question):
                            st.success("Вопрос удален")
                            st.rerun()
                        else:
                            st.error("Ошибка при удалении вопроса")
                with col3:
                    if st.button("Редактировать", key=f"edit_{i}"):
                        st.session_state[f"edit_mode_{i}"] = True
                if st.session_state.get(f"edit_mode_{i}", False):
                    new_text = st.text_area("Изменить вопрос", value=question, key=f"edit_text_{i}")
                    if st.button("Сохранить", key=f"save_edit_{i}"):
                        if new_text and new_text != question:
                            if question_manager.update_question(selected_test, question, new_text):
                                st.success("Вопрос обновлен")
                                st.session_state[f"edit_mode_{i}"] = False
                                st.rerun()
                            else:
                                st.error("Ошибка при обновлении вопроса")
                        else:
                            st.warning("Введите новый текст вопроса")
                    if st.button("Отмена", key=f"cancel_edit_{i}"):
                        st.session_state[f"edit_mode_{i}"] = False
        else:
            st.info("В этом тесте пока нет вопросов")
    
    # Вкладка "Настройка моделей"
    with tab5:
        st.header("Настройка моделей (Демо)")
        
        # STT модели
        st.subheader("Модели распознавания речи (STT)")
        stt_model = st.selectbox(
            "Выберите STT модель",
            ["Whisper", "Vosk", "Google", "API", "Amazon"],
            key="stt_model"
        )
        
        if stt_model == "Whisper":
            st.text_input("Название модели", value="base")
        elif stt_model == "Vosk":
            st.text_input("Путь к модели")
        elif stt_model == "Google":
            st.text_input("Путь к credentials.json")
        elif stt_model == "API":
            st.text_input("API Endpoint")
            st.text_input("API Key")
        elif stt_model == "Amazon":
            st.text_input("AWS Access Key ID")
            st.text_input("AWS Secret Access Key")
            st.text_input("Region Name")
        
        # TTS модели
        st.subheader("Модели синтеза речи (TTS)")
        tts_model = st.selectbox(
            "Выберите TTS модель",
            ["Edge", "ElevenLabs", "Google", "API", "Amazon"],
            key="tts_model"
        )
        
        if tts_model == "Edge":
            st.text_input("Голос", value="ru-RU-DmitryNeural")
        elif tts_model == "ElevenLabs":
            st.text_input("API Key")
        elif tts_model == "Google":
            st.text_input("Путь к credentials.json")
        elif tts_model == "API":
            st.text_input("API Endpoint")
            st.text_input("API Key")
        elif tts_model == "Amazon":
            st.text_input("AWS Access Key ID")
            st.text_input("AWS Secret Access Key")
            st.text_input("Region Name")
        
        # LLM модели
        st.subheader("Языковые модели (LLM)")
        llm_model = st.selectbox(
            "Выберите LLM модель",
            ["Mistral", "OpenAI", "Claude", "Llama", "Yandex", "API"],
            key="llm_model"
        )
        
        if llm_model == "Mistral":
            st.text_input("API Key")
        elif llm_model == "OpenAI":
            st.text_input("API Key")
        elif llm_model == "Claude":
            st.text_input("API Key")
        elif llm_model == "Llama":
            st.text_input("Hugging Face Model ID")
            st.text_input("Hugging Face Token")
            st.text_input("Локальный путь к модели")
        elif llm_model == "Yandex":
            st.text_input("Путь к service_account.json")
        elif llm_model == "API":
            st.text_input("API Endpoint")
            st.text_input("API Key")
        
        if st.button("Сохранить настройки моделей"):
            st.success("Настройки сохранены (демо)")

if __name__ == "__main__":
    admin_app()
