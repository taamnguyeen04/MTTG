
import streamlit as st
import time
from datetime import datetime
from config import load_data, save_data, text_to_speech, recognize_speech, send_email, RESULTS_FILE

def quiz_interface():
    st.header("🧠 Kiểm Tra Kiến Thức")
    questions = load_data("data/questions.json")
    st.session_state.quiz_answers = {}
    st.session_state.start_time = time.time()
    for idx, q in enumerate(questions[:3]):
        st.subheader(f"Câu {idx + 1}: {q['cau_hoi']}")
        st.radio("Chọn đáp án:", q["dap_an"], key=f"q_{idx}")

    if st.button("🎯 Nộp bài"):
        score = sum(
            1 for i, q in enumerate(questions[:3])
            if st.session_state.get(f"q_{i}") == q["dap_an"][ord(q["dap_an_dung"]) - ord("A")]
        )
        st.success(f"Bạn đạt {score}/{len(questions[:3])} điểm")
        result = {
            "score": score,
            "total": len(questions[:3]),
            "timestamp": datetime.now().isoformat()
        }
        results = load_data(RESULTS_FILE)
        results.append(result)
        save_data(RESULTS_FILE, results)

def support_page():
    st.header("📧 Hỗ Trợ Học Tập")
    if st.button("🎤 Ghi nội dung"):
        text_to_speech("Hãy nói nội dung bạn cần hỗ trợ")
        content = recognize_speech()
        st.session_state.support_content = content

    email_content = st.text_area("Nội dung email:", value=st.session_state.get("support_content", ""))
    if st.button("📤 Gửi email"):
        send_email("Yêu cầu hỗ trợ học tập", email_content, "nguyentranminhtam04@gmail.com")
        st.success("Đã gửi email thành công!")
