
import streamlit as st
from lessons import show_lessons
from flashcards import show_flashcards
from quiz_and_support import quiz_interface, support_page

st.set_page_config(page_title="Hệ thống học tập cho người khiếm thị", layout="wide")

def home_page():
    st.title("📚 Hệ thống học tập thông minh dành cho người khiếm thị")
    st.write("Chào mừng bạn đến với hệ thống hỗ trợ học tập tích hợp AI.")

def main():
    st.sidebar.title("🏫 Menu")
    choice = st.sidebar.radio("Chọn chức năng:", ["🏠 Trang chủ", "📚 Bài học", "🧠 Kiểm tra", "📧 Hỗ trợ"])

    if choice == "🏠 Trang chủ":
        home_page()
    elif choice == "📚 Bài học":
        show_lessons()
    elif choice == "🧠 Kiểm tra":
        quiz_interface()
    elif choice == "📧 Hỗ trợ":
        support_page()

if __name__ == "__main__":
    main()
