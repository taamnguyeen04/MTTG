import streamlit as st
from utils import send_email, text_to_speech, recognize_speech
import time
def support_page():
    # """Trang hỗ trợ hoàn toàn bằng giọng nói"""
    # """Hiển thị trang hỗ trợ gửi mail cho giáo viên bằng giọng nói"""
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
    # st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📧 Hỗ trợ học tập</h1>", unsafe_allow_html=True)

    TEACHERS = {
        "Nguyễn Trần Minh Tâm": "nguyentranminhtam04@gmail.com",
        "Đinh Thị Giàu": "dinhthigiau.contact@gmail.com"
    }

    # Khởi tạo session state
    if 'voice_support' not in st.session_state:
        st.session_state.voice_support = {
            "step": "select_teacher",
            "teacher": None,
            "content": "",
            "confirmations": 0,
            "first_prompt": True
        }

    # Xử lý luồng giọng nói
    if st.session_state.voice_support["first_prompt"]:
        text_to_speech("Xin hãy nói tên giáo viên bạn muốn liên hệ")
        st.session_state.voice_support["first_prompt"] = False
        # return

    # Bước 1: Chọn giáo viên
    if st.session_state.voice_support["step"] == "select_teacher":
        # teacher_name = recognize_speech()
        time.sleep(3)
        teacher_name = "Minh Tâm"
        if teacher_name:
            best_match = process_teacher_input(teacher_name, TEACHERS)
            if best_match:
                st.session_state.voice_support["teacher"] = best_match
                text_to_speech(f"Bạn đã chọn giáo viên {best_match}. Hãy nói nội dung cần gửi")
                st.session_state.voice_support["step"] = "record_content"
            else:
                text_to_speech("Không tìm thấy giáo viên phù hợp. Vui lòng nói lại tên giáo viên")
        # return

    # Bước 2: Ghi nhận nội dung
    if st.session_state.voice_support["step"] == "record_content":
        # content = recognize_speech()
        time.sleep(3)
        content = "dạ em cần thầy hỗ trợ"
        if content:
            st.session_state.voice_support["content"] = content
            text_to_speech(f"Nội dung của bạn là: {content}. Bạn có muốn gửi ngay không? Hãy nói Có hoặc Không")
            st.session_state.voice_support["step"] = "confirmation"
        # return

    # Bước 3: Xác nhận
    if st.session_state.voice_support["step"] == "confirmation":
        # confirm = recognize_speech()
        time.sleep(3)
        confirm = "có"
        if confirm:
            if "có" in confirm.lower():
                # Gửi email
                success = send_email(
                    subject="Yêu cầu hỗ trợ từ học sinh",
                    body=st.session_state.voice_support["content"],  # Đổi content -> body
                    receiver_email=TEACHERS[st.session_state.voice_support["teacher"]]
                    # Đổi recipient -> receiver_email
                )
                if success:
                    text_to_speech("Đã gửi email thành công cho giáo viên!")
                else:
                    text_to_speech("Có lỗi xảy ra khi gửi email. Vui lòng thử lại sau")

                # Reset trạng thái
                st.session_state.voice_support = {
                    "step": "select_teacher",
                    "teacher": None,
                    "content": "",
                    "confirmations": 0,
                    "first_prompt": True
                }
            else:
                text_to_speech("Đã hủy gửi email. Vui lòng bắt đầu lại")
                st.session_state.voice_support["step"] = "select_teacher"
        # return


def process_teacher_input(voice_input, teachers):
    """Xử lý tên giáo viên từ đầu vào giọng nói"""
    voice_input = voice_input.lower().replace("cô", "").replace("thầy", "").strip()
    best_score = 0
    best_match = None

    for name in teachers.keys():
        clean_name = name.lower().replace("cô", "").replace("thầy", "").strip()
        score = sum(
            1 for word in voice_input.split()
            if word in clean_name.split()
        )

        if score > best_score:
            best_score = score
            best_match = name

    return best_match if best_score > 0 else None