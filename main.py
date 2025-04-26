import streamlit as st
from pages.home_page import home_page
from pages.lessons_page import show_lessons
from pages.quiz_page import quiz_interface
from pages.support_page import support_page

st.set_page_config(page_title="Hệ thống học tập", page_icon="📚", layout="wide")

menu = st.sidebar.radio("Chọn chức năng:", ["🏠 Trang chủ", "📚 Bài học", "🧠 Kiểm tra kiến thức", "📧 Hỗ trợ học tập"])

if menu == "🏠 Trang chủ":
    home_page()
elif menu == "📚 Bài học":
    show_lessons()
elif menu == "🧠 Kiểm tra kiến thức":
    quiz_interface()
elif menu == "📧 Hỗ trợ học tập":
    support_page()