import streamlit as st
from streamlit_shortcuts import add_keyboard_shortcuts

from pages.home_page import home_page
from pages.lessons_page import show_lessons
from pages.quiz_page import quiz_interface
from pages.support_page import support_page

# ====== Cấu hình chung ======
st.set_page_config(page_title="Hệ thống học tập", page_icon="📚", layout="wide")

# ====== Khởi tạo session state ======
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Trang chủ"

# ====== Gán hotkey ======
add_keyboard_shortcuts({
    'Alt+P': 'Trang chủ',
    'Alt+B': 'Bài học',
    'Alt+K': 'Kiểm tra',
    'Alt+H': 'Hỗ trợ',
})

# ====== Sidebar navigation ======
with st.sidebar:
    st.header("🔎 Điều hướng nhanh")

    # Tạo nút cho từng trang
    if st.button("🏠 Trang chủ"):
        st.session_state.current_page = "🏠 Trang chủ"

    if st.button("📚 Bài học"):
        st.session_state.current_page = "📚 Bài học"

    if st.button("🧠 Kiểm tra kiến thức"):
        st.session_state.current_page = "🧠 Kiểm tra kiến thức"

    if st.button("📧 Hỗ trợ học tập"):
        st.session_state.current_page = "📧 Hỗ trợ học tập"

# ====== Xử lý phím tắt nếu có ======
if "keyboard_shortcuts" in st.session_state:
    shortcut = st.session_state["keyboard_shortcuts"]

    if shortcut == "Trang chủ":
        st.session_state.current_page = "🏠 Trang chủ"
    elif shortcut == "Bài học":
        st.session_state.current_page = "📚 Bài học"
    elif shortcut == "Kiểm tra":
        st.session_state.current_page = "🧠 Kiểm tra kiến thức"
    elif shortcut == "Hỗ trợ":
        st.session_state.current_page = "📧 Hỗ trợ học tập"

# ====== Điều hướng trang ======
if st.session_state.current_page == "🏠 Trang chủ":
    home_page()
elif st.session_state.current_page == "📚 Bài học":
    show_lessons()
elif st.session_state.current_page == "🧠 Kiểm tra kiến thức":
    quiz_interface()
elif st.session_state.current_page == "📧 Hỗ trợ học tập":
    support_page()
