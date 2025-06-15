import streamlit as st
import os

st.set_page_config(
    page_title="AI Interviewer",
    page_icon="🎤",
    layout="wide"
)

st.title("AI Интервьюер")
st.write("Добро пожаловать в приложение AI Интервьюер. Пожалуйста, выберите интерфейс:")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Пользовательский интерфейс")
    st.write("Пройдите интервью с вопросами и обратной связью от ИИ.")
    if st.button("Перейти в пользовательский интерфейс", use_container_width=True):
        st.switch_page("pages/user_interface.py")

with col2:
    st.subheader("Административный интерфейс")
    st.write("Управляйте тестами и вопросами, просматривайте результаты.")
    if st.button("Перейти в административный интерфейс", use_container_width=True):
        st.switch_page("pages/admin_interface.py") 