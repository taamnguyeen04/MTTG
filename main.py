import streamlit as st
import json
import random
import os

# File lưu câu hỏi & kết quả
QUESTIONS_FILE = "data/test.json"
RESULTS_FILE = "results.json"


# Load câu hỏi từ file JSON
def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Lưu kết quả vào file JSON
def save_result(username, score):
    results = []
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r", encoding="utf-8") as file:
            results = json.load(file)

    results.append({"username": username, "score": score})

    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)


# Cấu hình giao diện
st.set_page_config(page_title="Quiz Python", page_icon="🧠", layout="centered")

st.markdown(
    """
    <style>
        .big-title {
            font-size: 35px;
            font-weight: bold;
            text-align: center;
            color: #4CAF50;
        }
        .question {
            font-size: 20px;
            font-weight: bold;
            color: #FF5722;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<p class='big-title'>🧠 Quiz Python</p>", unsafe_allow_html=True)

# Khởi tạo session state nếu chưa có
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Nhập tên người chơi
username = st.text_input("Nhập tên của bạn:", placeholder="Nhập tên...")

if username:
    if not st.session_state.questions:
        st.session_state.questions = load_questions()
        random.shuffle(st.session_state.questions)  # Xáo trộn câu hỏi

    # Hiển thị các câu hỏi
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f"<p class='question'>{i + 1}. {q['cau_hoi']}</p>", unsafe_allow_html=True)

        # Tạo key duy nhất cho mỗi câu hỏi
        question_key = f"q_{i}"

        # Nếu chưa có câu trả lời cho câu hỏi này trong session state, khởi tạo với None
        if question_key not in st.session_state.answers:
            st.session_state.answers[question_key] = None

        # Hiển thị radio button và lưu câu trả lời vào session state
        st.session_state.answers[question_key] = st.radio(
            "Chọn đáp án:",
            q["dap_an"],
            index=None if st.session_state.answers[question_key] is None else q["dap_an"].index(
                st.session_state.answers[question_key]),
            key=question_key
        )

    if st.button("🎯 Nộp bài", help="Nhấn để xem điểm số") and not st.session_state.submitted:
        st.session_state.submitted = True
        score = 0

        for i, q in enumerate(st.session_state.questions):
            question_key = f"q_{i}"
            selected_answer = st.session_state.answers.get(question_key)

            if selected_answer == q["dap_an"][ord(q["dap_an_dung"]) - ord("A")]:
                score += 1

        save_result(username, score)
        st.success(f"🎉 {username}, bạn đã hoàn thành! Điểm số: {score}/{len(st.session_state.questions)}")

        # Hiển thị bảng xếp hạng
        st.subheader("📊 Bảng xếp hạng:")
        results = []
        if os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, "r", encoding="utf-8") as file:
                results = json.load(file)

        for r in sorted(results, key=lambda x: x["score"], reverse=True):
            st.write(f"🏅 {r['username']}: {r['score']} điểm")
else:
    st.warning("⚠️ Vui lòng nhập tên trước khi làm bài!")