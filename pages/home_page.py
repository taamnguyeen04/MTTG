import streamlit as st
from streamlit_shortcuts import add_keyboard_shortcuts
import time
from utils import text_to_speech

def home_page():
    """Trang chủ hỗ trợ tư duy học tập và tư thế ngồi thông minh cho người khiếm thị."""

    # ===== Khởi tạo session state =====
    if "voice_mode" not in st.session_state:
        st.session_state.voice_mode = True  # Mặc định bật Voice
    if "voice_mode_key" not in st.session_state:
        st.session_state.voice_mode_key = 1
    if "pending_alert" not in st.session_state:
        st.session_state.pending_alert = None
    if "selected_class" not in st.session_state:
        st.session_state.selected_class = None
    if "page_intro_read" not in st.session_state:
        st.session_state.page_intro_read = False

    # ====== Layout ======
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(76,175,80,0.3);
    }
    .feature-card, .guide-step, .contact-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-header">
        <h1>📚 Hệ thống hỗ trợ tư duy học tập và tư thế ngồi thông minh</h1>
    </div>
    """, unsafe_allow_html=True)

    # ====== Đọc Intro 1 lần ======
    if not st.session_state.page_intro_read:
        intro = """
        Bạn đang ở Trang Chủ.
        Chế độ hiện tại của bạn là chế độ giọng nói
        Các phím tắt:
        Alt+V: Bật hoặc tắt chế độ giọng nói.
        Alt+L: Mở khu vực chọn lớp học.
        Alt+1 đến Alt+5: Chọn lớp học.
        Alt+P: Trang chủ.
        Alt+B: Bài học.
        Alt+K: Kiểm tra.
        Alt+H: Hỗ trợ học tập.
        """
        text_to_speech(intro)
        st.session_state.page_intro_read = True
        time.sleep(2)

    # ====== Các hàm xử lý ======
    def toggle_voice_mode():
        st.session_state.voice_mode = not st.session_state.voice_mode
        st.session_state.voice_mode_key += 1  # Tăng key để ép toggle update
        if st.session_state.voice_mode:
            text_to_speech("Đã bật chế độ giọng nói.")
        else:
            text_to_speech("Đã chuyển sang chế độ bàn phím.")
        time.sleep(1)

    def area_choose_class():
        text_to_speech("Bạn đang ở khu vực chọn lớp học. Nhấn Alt cộng số lớp từ 1 đến 5.")

    def area_open_guide():
        guide = """
        Hướng dẫn nhanh các phím tắt:
        Alt+V: Chuyển chế độ giọng nói hoặc bàn phím.
        Alt+L: Mở chọn lớp học.
        Alt+X: Xem hướng dẫn 
        Alt+1 đến Alt+5: Chọn lớp học.
        Alt+P: Trang chủ.
        Alt+B: Bài học.
        Alt+K: Kiểm tra kiến thức.
        Alt+H: Hỗ trợ học tập.
        """
        text_to_speech(guide)

    def select_class(class_num):
        st.session_state.selected_class = class_num
        text_to_speech(f"Bạn đã chọn Lớp {class_num}.")
        time.sleep(1)

    def switch_page(page_name):
        st.session_state.current_page = page_name

    def alert_voice_mode_on():
        text_to_speech("Bạn đang ở chế độ giọng nói. Vui lòng chuyển sang chế độ bàn phím để sử dụng phím tắt.")

    # ====== Toggle chế độ ======
    st.toggle(
        "🎤 Bật/Tắt chế độ giọng nói",
        value=st.session_state.voice_mode,
        key=st.session_state.voice_mode_key,
    )
    st.button("🔀 Thay đổi chế độ điều khiển", on_click=toggle_voice_mode)

    # ====== Các khu vực chính ======
    st.header("🔀 Điều khiển hệ thống")
    st.button("Chọn lớp học", on_click=area_choose_class)
    st.button("Xem hướng dẫn sử dụng", on_click=area_open_guide)
    st.markdown("<h1>🏠 Trang chủ</h1>", unsafe_allow_html=True)
    st.button("📚 Chuyển sang Bài học", on_click=lambda: switch_page("📚 Bài học"))
    st.button("🧠 Chuyển sang Kiểm tra kiến thức", on_click=lambda: switch_page("🧠 Kiểm tra kiến thức"))
    st.button("📧 Chuyển sang Hỗ trợ học tập", on_click=lambda: switch_page("📧 Hỗ trợ học tập"))

    # ====== Gán Hotkey ======
    add_keyboard_shortcuts({
        'Alt+V': 'Thay đổi chế độ điều khiển',
        'Alt+L': 'Chọn lớp học',
        'Alt+X': 'Xem hướng dẫn sử dụng',
        'Alt+1': 'Lớp 1',
        'Alt+2': 'Lớp 2',
        'Alt+3': 'Lớp 3',
        'Alt+4': 'Lớp 4',
        'Alt+5': 'Lớp 5',
        "Alt+P": lambda: switch_page("🏠 Trang chủ"),
        "Alt+B": lambda: switch_page("📚 Bài học"),
        "Alt+K": lambda: switch_page("🧠 Kiểm tra kiến thức"),
        "Alt+H": lambda: switch_page("📧 Hỗ trợ học tập"),
    })

    # ====== Các lớp học ======
    st.header("📚 Các lớp học")
    cols = st.columns(3)
    for i in range(1, 6):
        with cols[(i - 1) % 3]:
            st.button(f"🧮 Lớp {i}", key=f"class_btn_{i}", on_click=select_class, args=(i,))

    # ====== Hướng dẫn ======
    st.header("📘 Hướng dẫn sử dụng nhanh")
    with st.expander("Mở hướng dẫn", expanded=False):
        st.markdown("""
        <div class="guide-step">
            <h4>🎯 Phím tắt:</h4>
            <ul>
                <li><b>Alt+V</b>: Bật/Tắt chế độ giọng nói</li>
                <li><b>Alt+L</b>: Mở khu vực chọn lớp học</li>
                <li><b>Alt+1 → Alt+5</b>: Chọn lớp 1 đến lớp 5</li>
                <li><b>Alt+P</b>: Trang chủ</li>
                <li><b>Alt+B</b>: Bài học</li>
                <li><b>Alt+K</b>: Kiểm tra kiến thức</li>
                <li><b>Alt+H</b>: Hỗ trợ học tập</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Thông tin liên hệ
    st.markdown("""
    <div class="contact-card">
        <h3 style="margin-top:0">📬 Liên Hệ Hỗ Trợ</h3>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap:1rem;">
            <div style="padding:1rem; background:#fff; border-radius:10px;">
                <h4 style="margin:0 0 0.5rem 0">💌 Email</h4>
                <p style="margin:0">support@hocsinhthongminh.vn</p>
            </div>
            <div style="padding:1rem; background:#fff; border-radius:10px;">
                <h4 style="margin:0 0 0.5rem 0">📞 Hotline</h4>
                <p style="margin:0">1900 1234 (24/7)</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # # text_to_speech(intro_text)
    # time.sleep(1)
    # text_to_speech("Bạn học lớp mấy?")
    # # speech = recognize_speech().lower()
    # time.sleep(2)
    # speech = "lớp 4"
    # # Nhận diện lớp học
    # for i in range(1, 6):
    #     if f"lớp {i}" in speech:
    #         text_to_speech(f"Bạn đã chọn lớp {i}")
    #         st.session_state.selected_class = i
    #         break

         # ====== Xử lý Hotkey ======
    if "keyboard_shortcuts" in st.session_state:
        shortcut_pressed = st.session_state["keyboard_shortcuts"]

        if st.session_state.voice_mode:
            st.session_state.pending_alert = "Bạn đang ở chế độ giọng nói. Vui lòng chuyển sang chế độ bàn phím để sử dụng phím tắt."
        else:
            if shortcut_pressed == "Thay đổi chế độ điều khiển":
                toggle_voice_mode()
            elif shortcut_pressed == "Chọn lớp học":
                area_choose_class()
            elif shortcut_pressed == "Xem hướng dẫn sử dụng":
                area_open_guide()
            elif shortcut_pressed == "Lớp 1":
                select_class(1)
            elif shortcut_pressed == "Lớp 2":
                select_class(2)
            elif shortcut_pressed == "Lớp 3":
                select_class(3)
            elif shortcut_pressed == "Lớp 4":
                select_class(4)
            elif shortcut_pressed == "Lớp 5":
                select_class(5)
    # ====== Thực thi Pending Alert nếu có ======
    if st.session_state.pending_alert:
        text_to_speech(st.session_state.pending_alert)
        st.session_state.pending_alert = None  # Xóa alert sau khi đọc
