import streamlit as st
import json
import random
from datetime import datetime
import pandas as pd
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from io import BytesIO
import speech_recognition as sr
from gtts import gTTS
import os
import pygame

# ========== CẤU HÌNH HỆ THỐNG ==========
st.set_page_config(
    page_title="Hệ thống kích thích tư duy học tập và hỗ trợ điều chỉnh tư thế ngồi thông minh dành cho người khiếm thị",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Đường dẫn file
LESSONS_FILE = "data/lessons.json"
QUESTIONS_FILE = "data/questions.json"
RESULTS_FILE = "results.json"
FLASHCARDS_FILE = "data/flashcards.json"
os.makedirs("data", exist_ok=True)

# Khởi tạo pygame mixer
pygame.mixer.init()


# ========== CÁC HÀM TIỆN ÍCH ==========
def load_data(file_path):
    """Tải dữ liệu từ file JSON"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def load_flashcards():
    if os.path.exists(FLASHCARDS_FILE):
        with open(FLASHCARDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

flashcards = load_flashcards()
random.shuffle(flashcards)

def save_data(file_path, data):
    """Lưu dữ liệu vào file JSON"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def send_email(subject, body, receiver_email):
    """Gửi email sử dụng SMTP"""
    sender_email = "tam.nguyentranminh04@hcmut.edu.vn"
    password = "toeu xjcj wgog lyav"  # Thay bằng App Password của bạn

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception as e:
        st.error(f"Lỗi khi gửi email: {str(e)}")
        return False


def text_to_speech(text, filename="temp_speech.mp3", language='vi'):
    """Chuyển văn bản thành giọng nói và phát"""
    try:
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except PermissionError:
                print("Không thể xóa file cũ")
                return False
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        return True
    except Exception as e:
        st.error(f"Lỗi trong text_to_speech: {str(e)}")
        return False


def recognize_speech():
    """
    Nhận diện giọng nói và chuyển đổi thành văn bản.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Nói gì đó: ")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="vi-VI")
        return text
    except sr.UnknownValueError:
        return "Không nhận diện được giọng nói."
    except sr.RequestError:
        return "Lỗi kết nối đến dịch vụ nhận diện giọng nói."


def show_flashcards():
    # Xác định loại flashcard dựa trên môn học được chọn
    if st.session_state.selected_subject == "Tiếng Anh":
        flashcards = load_data(FLASHCARDS_FILE)
        lang = "en"
    elif st.session_state.selected_subject == "Tiếng Nhật":
        flashcards = load_data("data/flashcards_japanese.json")
        lang = "ja"
    else:
        st.warning("Flashcard không khả dụng cho môn học này")
        return

    random.shuffle(flashcards)

    # CSS để tạo hiệu ứng lật thẻ (giữ nguyên như cũ)
    st.markdown(
        """
        <style>
            .flashcard-container {
                perspective: 1000px;
                width: 300px;
                height: 200px;
                margin: 0 auto;
                cursor: pointer;
            }
            .flashcard {
                width: 100%;
                height: 100%;
                position: relative;
                transform-style: preserve-3d;
                transition: transform 0.5s;
            }
            .flashcard:hover {
                transform: rotateY(180deg);
            }
            .flashcard-front, .flashcard-back {
                position: absolute;
                width: 100%;
                height: 100%;
                backface-visibility: hidden;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 36px;
                font-weight: bold;
                color: #fff;
                border-radius: 15px;
            }
            .flashcard-front {
                background-color: #FFEB3B;
            }
            .flashcard-back {
                background-color: #03A9F4;
                transform: rotateY(180deg);
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"<h1 style='text-align: center; color: #4CAF50;'>🃏 Flashcard {st.session_state.selected_subject} (Lật thẻ)</h1>",
        unsafe_allow_html=True)

    # Trạng thái thẻ
    if "index" not in st.session_state:
        st.session_state.index = 0
        st.session_state.should_speak = True
    elif "last_index" not in st.session_state or st.session_state.last_index != st.session_state.index:
        st.session_state.should_speak = True
        st.session_state.last_index = st.session_state.index
    else:
        st.session_state.should_speak = False

    card = flashcards[st.session_state.index]
    word = card["word"]
    meaning = card["meaning"]

    # Thêm romaji nếu có (cho tiếng Nhật)
    romaji = card.get("romaji", "")

    # Hiển thị flashcard với hiệu ứng lật
    st.markdown(f"""
    <div class="flashcard-container" onclick="window.location.reload();">
        <div class="flashcard">
            <div class="flashcard-front">{word}</div>
            <div class="flashcard-back">{meaning}{f"<br><small>{romaji}</small>" if romaji else ""}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chỉ đọc từ khi chuyển sang thẻ mới
    if st.session_state.should_speak:
        text_to_speech(word, filename="japanese.mp3", language=lang)
        text_to_speech(meaning, filename="vietnamese.mp3", language="vi")
        if romaji:
            text_to_speech(romaji, filename="romaji.mp3", language="en")

    # Nút tiếp theo
    if st.button("➡️ Tiếp theo"):
        st.session_state.index = (st.session_state.index + 1) % len(flashcards)
        st.rerun()

    # Hàm xử lý nhấn phím cách (space bar)
    st.markdown("""
    <script>
        window.addEventListener('keydown', function(event) {
            if (event.code === 'Space') {
                window.location.reload();
            }
        });
    </script>
    """, unsafe_allow_html=True)


# ========== TRANG CHỦ ==========
def home_page():
    """Hiển thị trang chủ giới thiệu hệ thống"""
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🏠 Hệ thống kích thích tư duy học tập và hỗ trợ điều chỉnh tư thế ngồi thông minh dành cho người khiếm thị</h1>",
                unsafe_allow_html=True)


    # Giới thiệu hệ thống
    with st.container():
        st.markdown("""
        <div style='background-color:#f0f2f6; padding:20px; border-radius:10px;'>
            <h3 style='color:#4CAF50;'>🌍 Giới thiệu hệ thống</h3>
            <p>Hệ thống kích thích tư duy học tập và hỗ trợ điều chỉnh tư thế ngồi thông minh dành cho người khiếm thị được thiết kế để hỗ trợ học sinh, đặc biệt là học sinh khiếm thị, 
            tiếp cận kiến thức dễ dàng thông qua đa dạng hình thức: văn bản, âm thanh, hình ảnh và tương tác.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔊 Nghe giới thiệu hệ thống"):
            intro_text = """
            Hệ thống kích thích tư duy học tập và hỗ trợ điều chỉnh tư thế ngồi thông minh cho người khiếm thị được thiết kế để hỗ trợ học sinh, 
            đặc biệt là học sinh khiếm thị, tiếp cận kiến thức dễ dàng thông qua 
            đa dạng hình thức: văn bản, âm thanh, hình ảnh và tương tác.
            """
            text_to_speech(intro_text)

    # Các tính năng chính
    st.markdown("### 🚀 Các tính năng chính")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='background-color:#e6f3ff; padding:15px; border-radius:10px; height:200px;'>
            <h4 style='color:#1a73e8;'>📚 Bài học</h4>
            <p>- Học qua văn bản, âm thanh, hình ảnh</p>
            <p>- Hỗ trợ đọc to nội dung</p>
            <p>- Gửi câu hỏi trực tiếp</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background-color:#e6f3ff; padding:15px; border-radius:10px; height:200px;'>
            <h4 style='color:#1a73e8;'>🧠 Kiểm tra kiến thức</h4>
            <p>- Làm bài quiz trắc nghiệm</p>
            <p>- Trả lời bằng giọng nói</p>
            <p>- Xem kết quả ngay lập tức</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='background-color:#e6f3ff; padding:15px; border-radius:10px; height:200px;'>
            <h4 style='color:#1a73e8;'>👁️ Hỗ trợ học sinh khiếm thị</h4>
            <p>- Điều khiển bằng giọng nói</p>
            <p>- Phản hồi âm thanh</p>
            <p>- Giao diện thân thiện</p>
        </div>
        """, unsafe_allow_html=True)

    # Hướng dẫn sử dụng
    with st.expander("📖 Hướng dẫn sử dụng"):
        st.markdown("""
        ### Cách sử dụng hệ thống:

        1. **Bài học**:
           - Chọn môn học từ danh sách
           - Chọn bài học từ các tab
           - Nhấn nút 🔊 để nghe nội dungchào mưng
           - Nhấn nút 🎤 để điều khiển bằng giọng nói

        2. **Kiểm tra kiến thức**:
           - Nhập tên để bắt đầu bài kiểm tra
           - Trả lời câu hỏi bằng cách chọn đáp án hoặc nói
           - Xem kết quả sau khi hoàn thành

        3. **Kết quả học tập**:
           - Xem lịch sử làm bài
           - Nghe kết quả bằng giọng nói
           - Tải xuống báo cáo
        """)

        if st.button("🔊 Nghe hướng dẫn sử dụng"):
            guide_text = """
            Hướng dẫn sử dụng hệ thống:
            1. Bài học: Chọn môn học và bài học từ danh sách, nhấn nút loa để nghe nội dung.
            2. Kiểm tra kiến thức: Nhập tên để bắt đầu, trả lời câu hỏi bằng cách chọn hoặc nói đáp án.
            3. Kết quả học tập: Xem và nghe kết quả các bài kiểm tra đã làm.
            """
            text_to_speech(guide_text)

    # Thông tin liên hệ
    st.markdown("""
    ### 📧 Liên hệ hỗ trợ
    Nếu bạn cần hỗ trợ hoặc có câu hỏi, vui lòng liên hệ:
    - Email: nguyentranminhtam04@gmail.com
    - Số điện thoại: 0899781007
    """)


# ========== GIAO DIỆN BÀI HỌC ==========
def show_lessons():
    """Hiển thị giao diện bài học với các card môn học có thể chọn được"""
    st.markdown("""
    <style>
        /* CSS tùy chỉnh cho toàn bộ trang */
        .main-title {
            text-align: center; 
            color: #4CAF50; 
            margin-bottom: 30px;
            font-size: 2.2rem;
            font-weight: 600;
        }
        .subject-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .subject-card {
            aspect-ratio: 1 / 1;
            border-radius: 12px;
            background: linear-gradient(145deg, #4CAF50 0%, #81C784 100%);
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border: none;
            padding: 20px;
            text-align: center;
        }
        .subject-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
            background: linear-gradient(145deg, #388E3C 0%, #66BB6A 100%);
        }
        .subject-card:active {
            transform: translateY(0);
        }
        .subject-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }
        .select-prompt {
            text-align: center;
            font-size: 1.2rem;
            color: #555;
            margin-bottom: 10px;
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .flashcard-btn {
            background: linear-gradient(145deg, #2196F3 0%, #03A9F4 100%) !important;
            color: white !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            padding: 15px 25px !important;
            border-radius: 12px !important;
            margin: 20px auto !important;
            display: block !important;
            width: 80% !important;
            box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3) !important;
        }
        .flashcard-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(33, 150, 243, 0.4) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">📚 Bài Học</h1>', unsafe_allow_html=True)

    lessons = load_data(LESSONS_FILE)
    if not lessons:
        st.markdown('<div class="empty-state">Hiện chưa có bài học nào được tạo!</div>', unsafe_allow_html=True)
        return

    # Lấy danh sách môn học và sắp xếp theo thứ tự alphabet
    subjects = sorted(list(set(lesson["mon_hoc"] for lesson in lessons)))

    # Icon tương ứng cho từng môn học
    subject_icons = {
        "Toán": "🧮",
        "Văn": "📝",
        "Tiếng Nhật": "🗾",
        "Anh": "🌎",
        "Lý": "⚛️",
        "Hóa": "🧪",
        "Sinh": "🧬",
        "Sử": "🏛️",
        "Địa": "🌍",
        "Đạo đức": "❤️",
        "GDCD": "⚖️",
        "Tin học": "💻",
        "Công nghệ": "🔧",
        "Mỹ thuật": "🎨",
        "Âm nhạc": "🎵",
        "Thể dục": "🏃"
    }

    st.markdown('<div class="select-prompt">Vui lòng chọn môn học</div>', unsafe_allow_html=True)

    # Hiển thị grid các môn học
    st.markdown('<div class="subject-grid">', unsafe_allow_html=True)

    # Tạo các card môn học có thể click được
    cols = st.columns(3)
    subjects_to_show = subjects + ["Tiếng Nhật"]  # Thêm môn Tiếng Nhật vào danh sách hiển thị

    for i, subject in enumerate(subjects_to_show):
    # for i, subject in enumerate(subjects):
        icon = subject_icons.get(subject, "📚")

        with cols[i % 3]:
            # Sử dụng st.button với HTML custom để có giao diện đẹp
            if st.button(
                f"{icon}\n\n{subject}",  # Sử dụng \n để xuống dòng
                key=f"subject_{subject}",
                # help=f"Chọn môn {subject}",
                use_container_width=True
            ):
                st.session_state.selected_subject = subject
                text_to_speech(f"Bạn đã chọn môn {subject}")
                st.rerun()  # Làm mới trang để hiển thị nội dung môn học

    st.markdown('</div>', unsafe_allow_html=True)

    # Kiểm tra nếu đã chọn môn học
    if 'selected_subject' not in st.session_state:
        st.markdown('<div class="empty-state">Vui lòng chọn một môn học từ danh sách trên</div>',
                    unsafe_allow_html=True)
        text_to_speech("Chọn môn học bạn muốn học")

        return

    # Nút quay lại chọn môn khác
    if st.button("↩️ Chọn môn khác"):
        del st.session_state.selected_subject
        st.rerun()

    # THÊM NÚT LUYỆN TẬP FLASHCARD NẾU LÀ MÔN TIẾNG ANH
    if st.session_state.selected_subject in ["Tiếng Anh", "Tiếng Nhật"]:
        btn_text = {
            "Tiếng Anh": "🃏 Luyện Tập Flashcard Tiếng Anh",
            "Tiếng Nhật": "🗾 Luyện Tập Flashcard Tiếng Nhật"
        }[st.session_state.selected_subject]

        if st.button(btn_text, key="flashcard_btn", use_container_width=True):
            st.session_state.show_flashcards = True
            st.rerun()

    # Nếu đang ở chế độ xem flashcard
    if st.session_state.get("show_flashcards"):
        print("*************************************************************************")
        show_flashcards()
        return

    # Phần hiển thị bài học sau khi chọn môn
    subject_lessons = [lesson for lesson in lessons if lesson["mon_hoc"] == st.session_state.selected_subject]
    if st.session_state.selected_subject == "Tiếng Nhật" and not subject_lessons:
        st.info("Hiện chưa có bài học nào cho môn Tiếng Nhật")

        # Chỉ hiển thị nút flashcard
        if st.button("🗾 Luyện Tập Flashcard Tiếng Nhật",
                     key="flashcard_btn_jp",
                     use_container_width=True):
            st.session_state.show_flashcards = True
            st.rerun()
        return
    # CSS cho tabs bài học
    st.markdown("""
    <style>
        .lesson-tabs {
            border-radius: 12px;
            overflow: hidden;
            margin-top: 30px;
        }
        .lesson-tab {
            padding: 15px 25px;
            font-size: 1.1rem;
        }
        .lesson-content {
            padding: 25px;
            background: #f9f9f9;
            border-radius: 0 0 12px 12px;
            margin-top: -1px;
        }
        .lesson-title {
            font-size: 1.6rem;
            color: #2E7D32;
            margin-bottom: 15px;
        }
        .lesson-desc {
            font-size: 1.1rem;
            line-height: 1.6;
            color: #444;
        }
    </style>
    """, unsafe_allow_html=True)

    # Tạo tabs bài học
    tab_titles = [lesson["ten_bai"] for lesson in subject_lessons]
    tabs = st.tabs(tab_titles)

    for i, tab in enumerate(tabs):
        with tab:
            lesson = subject_lessons[i]
            st.markdown(f'<div class="lesson-title">{lesson["ten_bai"]}</div>', unsafe_allow_html=True)

            # Bố cục 2 cột
            col1, col2 = st.columns([1, 2])

            with col1:
                if "hinh_anh" in lesson:
                    st.image(lesson["hinh_anh"], use_container_width=True)

            with col2:
                if "mo_ta" in lesson:
                    st.markdown(f'<div class="lesson-desc">{lesson["mo_ta"]}</div>', unsafe_allow_html=True)

                if "noi_dung_text" in lesson:
                    with st.expander("📖 Nội dung bài học", expanded=True):
                        st.markdown(lesson["noi_dung_text"])
                        # Nhóm các nút chức năng
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(
                            "🔊 Đọc bài",
                            key=f"read_{i}",
                            # help="Nhấn để nghe nội dung bài học",
                            use_container_width=True
                    ):
                        text_to_speech(lesson.get("noi_dung_text", ""))

                with btn_col2:
                    if st.button(
                            "🎤 Giọng nói",
                            key=f"voice_{i}",
                            # help="Nhấn để điều khiển bằng giọng nói",
                            use_container_width=True
                    ):
                        text_to_speech("Hãy nói lệnh của bạn")
                        command = recognize_speech()
                        if command:
                            if "đọc bài" in command or "đọc nội dung" in command:
                                text_to_speech(lesson.get("noi_dung_text", ""))
                            elif "gửi câu hỏi" in command:
                                st.session_state.voice_question = True
            # Xử lý gửi câu hỏi
            if st.session_state.get("voice_question"):
                text_to_speech("Hãy nói câu hỏi của bạn")
                question = recognize_speech()
                if question:
                    email_content = f"""
                    Học viên có câu hỏi về bài học:
                    - Môn: {st.session_state.selected_subject}
                    - Bài: {lesson['ten_bai']}
                    - Câu hỏi: {question}
                    """
                    if send_email(f"Câu hỏi về bài {lesson['ten_bai']}", email_content,
                                  "nguyentranminhtam04@gmail.com"):
                        st.success("Đã gửi câu hỏi đến giáo viên!")
                        text_to_speech("Đã gửi câu hỏi đến giáo viên")
                    st.session_state.voice_question = False
# ========== GIAO DIỆN QUIZ ==========
def quiz_interface():
    """Giao diện làm bài quiz với lựa chọn môn học"""
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🧠 Kiểm tra kiến thức</h1>", unsafe_allow_html=True)

    # Khởi tạo session state
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = {
            "started": False,
            "subject_selected": False,
            "subject": None,
            "submitted": False,
            "questions": [],
            "answers": {},
            "start_time": None,
            "current_question": 0,
            "first_time_enter": True
        }

    # Phần chọn môn học nếu chưa chọn
    if st.session_state.quiz_state["first_time_enter"]:
        text_to_speech("Chọn môn học bạn muốn kiểm tra")
        st.session_state.quiz_state["first_time_enter"] = False  # Đánh dấu đã đọc
    if not st.session_state.quiz_state["subject_selected"]:
        st.markdown("### Chọn môn học bạn muốn kiểm tra:")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📐 Toán", use_container_width=True):
                st.session_state.quiz_state.update({
                    "subject": "toán",
                    "subject_selected": True
                })
                st.rerun()

        with col2:
            if st.button("❤️ Đạo đức", use_container_width=True):
                st.session_state.quiz_state.update({
                    "subject": "đạo đức",
                    "subject_selected": True
                })
                st.rerun()

        with col3:
            if st.button("🌎 Tiếng Anh", use_container_width=True):
                st.session_state.quiz_state.update({
                    "subject": "anh văn",
                    "subject_selected": True
                })
                st.rerun()
        return

    # Phần nhập tên nếu đã chọn môn nhưng chưa bắt đầu
    if not st.session_state.quiz_state["started"]:
        # Hiển thị thông báo chỉ 1 lần
        if "name_prompt_shown" not in st.session_state:
            text_to_speech("Bạn tên gì")
            st.session_state.name_prompt_shown = True

        # Nút nhập tên bằng giọng nói (đặt bên ngoài form)
        if st.button("🎤 Nhập tên bằng giọng nói", key="voice_name_btn"):
            text_to_speech("Xin hãy nói tên của bạn")
            recognized_name = recognize_speech()
            if recognized_name:
                # Xử lý tên nhận được từ giọng nói
                processed_name = recognized_name.strip().title()
                st.session_state.temp_recognized_name = processed_name
                st.rerun()

        # Form nhập tên chính
        with st.form("start_form"):
            # Nếu có tên từ giọng nói, điền vào ô input
            username = st.text_input(
                "Nhập tên của bạn:",
                value=st.session_state.get("temp_recognized_name", ""),
                placeholder="Tên của bạn...",
                max_chars=20
            )

            submitted = st.form_submit_button("Bắt đầu làm bài")

            if submitted:
                if username.strip():
                    # Xác định file câu hỏi dựa trên môn đã chọn
                    subject_file = {
                        "toán": "data/toan.json",
                        "đạo đức": "data/đạo đức.json",
                        "anh văn": "data/anh_van.json"
                    }.get(st.session_state.quiz_state["subject"], "data/questions.json")

                    st.session_state.quiz_state.update({
                        "started": True,
                        "username": username.strip(),
                        "start_time": time.time(),
                        "questions": load_data(subject_file)
                    })
                    random.shuffle(st.session_state.quiz_state["questions"])
                    text_to_speech(
                        f"Chào mừng {username.strip()} đến với bài kiểm tra môn {st.session_state.quiz_state['subject']}")
                    st.rerun()
                else:
                    st.error("Vui lòng nhập tên hợp lệ!")
                    text_to_speech("Vui lòng nhập tên hợp lệ")
        return

    # Làm bài quiz (phần này giữ nguyên như cũ)
    quiz_state = st.session_state.quiz_state
    questions = quiz_state["questions"]
    current_q = quiz_state["current_question"]

    if current_q < len(questions):
        question = questions[current_q]

        st.markdown(f"### Câu {current_q + 1}/{len(questions)}")
        st.markdown(f"**{question['cau_hoi']}**")

        # Đọc câu hỏi và đáp án
        # Đọc câu hỏi và đáp án
        if st.button(f"🔊 Đọc câu hỏi {current_q + 1}"):
            question_text = f"Câu {current_q + 1}: {question['cau_hoi']}"
            options = " ".join([f"Đáp án {chr(65 + i)}: {option}." for i, option in enumerate(question['dap_an'])])
            full_text = f"{question_text} {options}"
            text_to_speech(full_text)

        # Hiển thị hình ảnh nếu có
        if "hinh_anh" in question:
            st.image(question["hinh_anh"], width=300)
            # text_to_speech("Hình ảnh minh họa cho câu hỏi")

        # Hiển thị đáp án
        answer_key = f"q_{current_q}"
        if answer_key not in quiz_state["answers"]:
            quiz_state["answers"][answer_key] = None

        quiz_state["answers"][answer_key] = st.radio(
            "Chọn đáp án:",
            question["dap_an"],
            index=None if quiz_state["answers"][answer_key] is None else
            question["dap_an"].index(quiz_state["answers"][answer_key]),
            key=answer_key
        )

        # Nút trả lời bằng giọng nói
        if st.button(f"🎤 Trả lời bằng giọng nói - Câu {current_q + 1}"):
            text_to_speech("Hãy nói đáp án của bạn, A, B, C hoặc D")
            answer = recognize_speech().split(" ")[1]
            print(answer)
            if answer:
                if answer in ["a", "b", "c", "d"]:
                    selected_index = ord(answer.upper()) - ord("A")
                    if selected_index < len(question["dap_an"]):
                        quiz_state["answers"][answer_key] = question["dap_an"][selected_index]
                        st.success(f"Đã chọn đáp án {answer.upper()}")
                        text_to_speech(f"Đã chọn đáp án {answer.upper()}")
                    else:
                        st.warning("Đáp án không hợp lệ")
                        text_to_speech("Đáp án không hợp lệ")
                else:
                    st.warning("Không nhận diện được đáp án hợp lệ")
                    text_to_speech("Không nhận diện được đáp án hợp lệ")

        # Hiển thị giải thích đáp án (nếu đã chọn đáp án)
        if quiz_state["answers"][answer_key] is not None:
            # Kiểm tra xem câu trả lời đúng hay sai
            is_correct = (quiz_state["answers"][answer_key] ==
                          question["dap_an"][ord(question["dap_an_dung"]) - ord("A")])

            # Tạo expander cho giải thích
            with st.expander("📝 Giải thích đáp án", expanded=False):
                if "giai_thich" in question:
                    st.markdown(f"**Giải thích:** {question['giai_thich']}")

                    # Đọc giải thích bằng giọng nói
                    if st.button(f"🔊 Nghe giải thích - Câu {current_q + 1}"):
                        explanation_text = f"Giải thích: {question['giai_thich']}"
                        text_to_speech(explanation_text)
                else:
                    st.info("Không có giải thích cho câu hỏi này.")

                st.markdown(f"**Đáp án đúng:** {question['dap_an_dung']}")

                # Hiển thị thông báo đúng/sai
                if is_correct:
                    st.success("🎉 Bạn đã trả lời đúng!")
                else:
                    st.error("❌ Bạn đã trả lời sai.")

        # Nút điều hướng
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⏪ Câu trước", disabled=current_q == 0):
                quiz_state["current_question"] -= 1
                st.rerun()
        with col3:
            if st.button("⏩ Câu tiếp", disabled=current_q == len(questions) - 1):
                quiz_state["current_question"] += 1
                st.rerun()
        with col2:
            if st.button("🎯 Nộp bài", type="primary"):
                quiz_state["submitted"] = True
                quiz_state["end_time"] = time.time()
                st.rerun()

    # Xử lý sau khi nộp bài (giữ nguyên như cũ)
    if quiz_state["submitted"]:
        # Tính điểm
        score = sum(
            1 for i, q in enumerate(questions)
            if quiz_state["answers"].get(f"q_{i}") == q["dap_an"][ord(q["dap_an_dung"]) - ord("A")]
        )

        # Lưu kết quả (thêm thông tin môn học vào kết quả)
        time_taken = quiz_state["end_time"] - quiz_state["start_time"]
        results = load_data(RESULTS_FILE)
        results.append({
            "username": quiz_state["username"],
            "subject": quiz_state["subject"],
            "score": score,
            "total": len(questions),
            "time_taken": time_taken,
            "timestamp": datetime.now().isoformat()
        })
        save_data(RESULTS_FILE, results)

        # Hiển thị kết quả
        subject_name = {
            "toan": "Toán",
            "dao_duc": "Đạo đức",
            "anh_van": "Tiếng Anh"
        }.get(quiz_state["subject"], "Môn học")

        result_text = f"""
        {quiz_state['username']} đã hoàn thành bài kiểm tra môn {subject_name}!
        Điểm số: {score}/{len(questions)} ({score / len(questions) * 100:.1f}%)
        Thời gian: {int(time_taken // 60)} phút {int(time_taken % 60)} giây
        """
        st.success(result_text)
        text_to_speech(result_text)

        # Gửi email kết quả
        if st.button("📤 Gửi kết quả đến giáo viên"):
            email_content = f"""
            Học viên {quiz_state['username']} đã hoàn thành bài kiểm tra môn {subject_name}:
            - Điểm số: {score}/{len(questions)}
            - Tỉ lệ đúng: {score / len(questions) * 100:.1f}%
            - Thời gian làm bài: {int(time_taken // 60)} phút {int(time_taken % 60)} giây
            """
            if send_email(f"Kết quả bài kiểm tra {subject_name} của {quiz_state['username']}", email_content,
                          "nguyentranminhtam04@gmail.com"):
                st.success("Đã gửi kết quả đến giáo viên!")
                text_to_speech("Đã gửi kết quả đến giáo viên")

        if st.button("🔄 Làm lại bài"):
            st.session_state.quiz_state = {
                "started": False,
                "subject_selected": False,
                "subject": None,
                "questions": [],
                "answers": {}
            }
            st.rerun()


# ========== GIAO DIỆN HỖ TRỢ ==========
def support_page():
    """Hiển thị trang hỗ trợ gửi mail cho giáo viên bằng giọng nói"""
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📧 Hỗ trợ học tập</h1>", unsafe_allow_html=True)

    # Danh sách giáo viên
    TEACHERS = {
        "Nguyễn Trần Minh Tâm": "nguyentranminhtam04@gmail.com",
        "Đinh Thị Giàu": "dinhthigiau.contact@gmail.com"
    }

    # Khởi tạo session state nếu chưa có
    if 'support_state' not in st.session_state:
        st.session_state.support_state = {
            "selected_teacher": None,
            "email_content": "",
            "is_recording": False,
            "first_time_enter": True
        }

    # Phần chọn môn học nếu chưa chọn
    if st.session_state.support_state["first_time_enter"]:
        text_to_speech("Hỗ trợ học tập")
        st.session_state.support_state["first_time_enter"] = False  # Đánh dấu đã đọc
    # CSS tùy chỉnh
    st.markdown("""
    <style>
        .teacher-card {
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background-color: #f0f2f6;
            transition: all 0.3s;
        }
        .teacher-card:hover {
            background-color: #e0e5ec;
            transform: translateY(-2px);
        }
        .teacher-selected {
            background-color: #4CAF50 !important;
            color: white !important;
        }
        .voice-btn {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Phần 1: Chọn giáo viên
    st.markdown("### 1. Chọn giáo viên cần hỗ trợ")
    # text_to_speech("Chọn giáo viên cần hỗ trợ")
    # Tạo các card giáo viên
    cols = st.columns(2)
    for i, (teacher_name, teacher_email) in enumerate(TEACHERS.items()):
        with cols[i % 2]:
            is_selected = st.session_state.support_state["selected_teacher"] == teacher_name
            card_class = "teacher-card teacher-selected" if is_selected else "teacher-card"

            st.markdown(
                f"""
                <div class="{card_class}" onclick="window.location.href='?teacher={teacher_name}'">
                    <h4>{teacher_name}</h4>
                    <p>{teacher_email}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Nút chọn giáo viên bằng giọng nói
    if st.button("🎤 Chọn giáo viên bằng giọng nói", key="select_teacher_voice"):
        text_to_speech("Hãy nói tên giáo viên bạn muốn liên hệ")
        teacher_name = recognize_speech()
        if teacher_name:
            # Tìm giáo viên phù hợp nhất với tên được nói
            best_match = None
            highest_score = 0
            for name in TEACHERS.keys():
                score = sum(1 for word in teacher_name.split() if word.lower() in name.lower())
                if score > highest_score:
                    highest_score = score
                    best_match = name

            if best_match:
                st.session_state.support_state["selected_teacher"] = best_match
                st.success(f"Đã chọn giáo viên: {best_match}")
                text_to_speech(f"Đã chọn giáo viên {best_match}")
            else:
                st.warning("Không tìm thấy giáo viên phù hợp")
                text_to_speech("Không tìm thấy giáo viên phù hợp")

    # Hiển thị giáo viên đã chọn
    if st.session_state.support_state["selected_teacher"]:
        st.markdown(f"""
        <div style="background-color:#e8f5e9; padding:10px; border-radius:5px; margin:10px 0;">
            <b>Giáo viên đã chọn:</b> {st.session_state.support_state["selected_teacher"]}
            <br><b>Email:</b> {TEACHERS[st.session_state.support_state["selected_teacher"]]}
        </div>
        """, unsafe_allow_html=True)

    # Phần 2: Nhập nội dung email
    st.markdown("### 2. Nội dung cần hỗ trợ")

    # Nhập nội dung bằng giọng nói
    if st.button("🎤 Nhập nội dung bằng giọng nói", key="input_content_voice"):
        st.session_state.support_state["is_recording"] = True
        st.warning("Đang ghi âm... Hãy nói nội dung bạn muốn gửi")
        text_to_speech("Hãy nói nội dung bạn muốn gửi cho giáo viên")

        content = recognize_speech()
        if content:
            st.session_state.support_state["email_content"] = content
            st.session_state.support_state["is_recording"] = False
            st.success("Đã ghi nhận nội dung!")
            text_to_speech("Đã ghi nhận nội dung của bạn")

    # Hiển thị textarea để chỉnh sửa nội dung
    email_content = st.text_area(
        "Nội dung email:",
        value=st.session_state.support_state["email_content"],
        height=150,
        placeholder="Nhập nội dung bạn cần hỗ trợ..."
    )
    st.session_state.support_state["email_content"] = email_content

    # Phần 3: Gửi email
    st.markdown("### 3. Gửi yêu cầu hỗ trợ")

    if st.button("📤 Gửi email cho giáo viên", type="primary"):
        if not st.session_state.support_state["selected_teacher"]:
            st.error("Vui lòng chọn giáo viên!")
            text_to_speech("Vui lòng chọn giáo viên")
        elif not st.session_state.support_state["email_content"].strip():
            st.error("Vui lòng nhập nội dung!")
            text_to_speech("Vui lòng nhập nội dung")
        else:
            teacher_name = st.session_state.support_state["selected_teacher"]
            teacher_email = TEACHERS[teacher_name]
            email_content = st.session_state.support_state["email_content"]

            # Thêm thông tin người gửi vào nội dung email
            full_content = f"""
            Học sinh gửi yêu cầu hỗ trợ:
            - Giáo viên: {teacher_name}
            - Nội dung: 
            {email_content}
            """

            if send_email(f"Yêu cầu hỗ trợ từ học sinh", full_content, teacher_email):
                st.success("Đã gửi email thành công!")
                text_to_speech("Đã gửi email thành công cho giáo viên")

                # Reset nội dung sau khi gửi
                st.session_state.support_state["email_content"] = ""
            else:
                st.error("Gửi email thất bại!")
                text_to_speech("Gửi email không thành công")


# ========== GIAO DIỆN CHÍNH ==========
def main():
    st.sidebar.title("🏫 Hệ thống Học tập")
    menu = st.sidebar.radio(
        "Chọn chức năng:",
        ["🏠 Trang chủ", "📚 Bài học", "🧠 Kiểm tra kiến thức", "📧 Hỗ trợ học tập"]
    )

    # Đọc menu chức năng
    # if st.sidebar.button("🔊 Đọc menu"):
    #     text_to_speech(f"Bạn đang chọn {menu}")

    if menu == "🏠 Trang chủ":
        home_page()
    elif menu == "📚 Bài học":
        show_lessons()
    elif menu == "🧠 Kiểm tra kiến thức":
        quiz_interface()
    else:
        support_page()


if __name__ == "__main__":
    main()
    # Dọn dẹp khi thoát ứng dụng
    if pygame.mixer.get_init():
        pygame.mixer.quit()