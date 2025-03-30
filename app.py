import streamlit as st
from alo_email import send_email
from speech import listen_keyboard, text_to_speech_v2
# from stt import recognize_speech
import threading
import queue


def main():
    st.title("Ứng dụng Học tập cho Học sinh Khiếm thị")
    st.sidebar.header("Chọn chức năng")

    # Danh sách chức năng
    menu = {
        "Môn Đạo Đức": moral_lesson,
        "Môn Toán": math_lesson,
        "Môn Tiếng Anh": english_lesson,
        "Hỗ trợ Giao tiếp": communication_support
    }

    # Khởi tạo session_state nếu chưa có
    if "selected_menu" not in st.session_state:
        st.session_state.selected_menu = None

    # Tạo nút bấm chọn menu, lưu vào session_state
    for label, function in menu.items():
        if st.sidebar.button(label):
            st.session_state.selected_menu = label


    # Nếu đã chọn menu thì chạy tiếp, không quay lại main()
    if st.session_state.selected_menu:
        menu[st.session_state.selected_menu](st.session_state.selected_menu)

def moral_lesson(label):
    st.header("Môn Đạo Đức")
    text_to_speech_v2("Môn Đạo Đức")
    if st.button("Nghe bài học"):
        st.write("Chức năng chuyển bài học thành giọng nói")
        text_to_speech_v2("Chức năng chuyển bài học thành giọng nói")

    if st.button("Làm bài tập trắc nghiệm bằng giọng nói"):
        question = "Câu hỏi: Khi thấy bạn bị ngã, em sẽ làm gì? A. Giúp bạn dậy. B. Cười bạn. C. Bỏ đi."
        st.write(question)
        text_to_speech_v2(question)

        st.write("Hãy nói đáp án của bạn (A, B hoặc C)...")
        text_to_speech_v2("Hãy nói đáp án của bạn (A, B hoặc C)...")
        answer = recognize_speech()
        st.write("Bạn đã trả lời:", answer)

        if answer.upper() == "A":
            st.write("Chính xác! Em là người tốt bụng.")
            text_to_speech_v2("Chính xác! Em là người tốt bụng.")
        else:
            st.write("Sai rồi! Hãy chọn đáp án đúng là A.")
            text_to_speech_v2("Sai rồi! Hãy chọn đáp án đúng là A.")


def math_lesson(label):
    st.header("Môn Toán")
    text_to_speech_v2("Môn Toán")
    if st.button("Nghe bài toán"):
        st.text("Hệ thống sẽ đọc phép toán")
    if st.button("Trả lời bằng giọng nói"):
        text = recognize_speech()
        st.write("Bạn đã trả lời:", text)


def english_lesson(label):
    st.header("Môn Tiếng Anh")
    text_to_speech_v2("Môn Tiếng Anh")
    if st.button("Luyện phát âm"):
        st.text("Hệ thống sẽ đọc từ, học sinh lặp lại")
        text = recognize_speech()
        st.write("Bạn đã nói:", text)
    if st.button("Bài tập từ vựng"):
        st.text("Điền từ vào chỗ trống")


def communication_support(label):
    st.header("Hỗ trợ giao tiếp")
    text_to_speech_v2("Hỗ trợ giao tiếp")
    if st.button("Gửi email cho giáo viên"):
        text = recognize_speech()
        send_email(text)
        st.success("Email đã được gửi!")
    if st.button("Bật bàn phím phát âm thanh"):
        # listen_keyboard()
        st.success("Bàn phím đang hoạt động!")


if __name__ == "__main__":
    main()