import streamlit as st
from utils import load_data, text_to_speech, LESSONS_FILE, recognize_speech, send_email, show_flashcards

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