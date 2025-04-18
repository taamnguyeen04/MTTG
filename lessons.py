
import streamlit as st
from config import load_data, text_to_speech
from flashcards import show_flashcards

def show_lessons():
    lessons = load_data("data/lessons.json")
    st.title("📚 Bài Học")

    subjects = sorted(list(set(lesson["mon_hoc"] for lesson in lessons)))
    subject = st.selectbox("Chọn môn học", subjects)

    st.session_state.selected_subject = subject

    subject_lessons = [lesson for lesson in lessons if lesson["mon_hoc"] == subject]
    for lesson in subject_lessons:
        st.subheader(lesson["ten_bai"])
        st.write(lesson.get("mo_ta", ""))
        if st.button(f"🔊 Đọc bài - {lesson['ten_bai']}"):
            text_to_speech(lesson.get("noi_dung_text", ""))

    if subject in ["Tiếng Anh", "Tiếng Nhật"]:
        if st.button("🃏 Luyện tập Flashcard"):
            show_flashcards()
