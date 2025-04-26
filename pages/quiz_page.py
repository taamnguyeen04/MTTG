import streamlit as st
import random
import time
from utils import load_data, save_data, text_to_speech, recognize_speech, RESULTS_FILE, send_email
from datetime import datetime

def quiz_interface():
    """Giao diện làm bài quiz với lựa chọn môn học"""
    st.markdown(
        "<h1 style='text-align: center; color: #4CAF50;'>🧠 Kiểm tra kiến thức</h1>",
        unsafe_allow_html=True
    )

    # Khởi tạo trạng thái quiz nếu chưa có
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

    quiz_state = st.session_state.quiz_state

    # Chào mừng người dùng lần đầu
    if quiz_state["first_time_enter"]:
        text_to_speech("Chọn môn học bạn muốn kiểm tra")
        quiz_state["first_time_enter"] = False

    # Nếu chưa chọn môn, hiển thị tùy chọn
    if not quiz_state["subject_selected"]:
        st.markdown("### 📚 Vui lòng chọn môn học:")

        col1, col2, col3 = st.columns(3)
        subject_buttons = {
            "toán": col1.button("📐 Toán", use_container_width=True),
            "đạo đức": col2.button("❤️ Đạo đức", use_container_width=True),
            "anh văn": col3.button("🌎 Tiếng Anh", use_container_width=True)
        }

        # Nếu người dùng click chọn môn học
        for subject, clicked in subject_buttons.items():
            if clicked:
                quiz_state["subject"] = subject
                quiz_state["subject_selected"] = True
                st.rerun()

        # Hoặc chọn bằng giọng nói
        if st.button("🎤 Giọng nói"):
            text_to_speech("Hãy nói tên môn học: Toán, Đạo đức hoặc Tiếng Anh")
            # spoken_subject = recognize_speech().lower()
            time.sleep(2)
            spoken_subject = "đạo đức"

            # Ghép các từ có thể nói thành tên chuẩn
            if "toán" in spoken_subject:
                selected_subject = "toán"
            elif "đạo đức" in spoken_subject or "daoduc" in spoken_subject:
                selected_subject = "đạo đức"
            elif "tiếng anh" in spoken_subject or "anh văn" in spoken_subject:
                selected_subject = "anh văn"
            else:
                selected_subject = None

            if selected_subject:
                quiz_state["subject"] = selected_subject
                quiz_state["subject_selected"] = True
                text_to_speech(f"Đã chọn môn {selected_subject}")
                st.rerun()
            else:
                text_to_speech("Không nhận diện được môn học. Vui lòng thử lại.")
        return

    # Phần nhập tên nếu đã chọn môn nhưng chưa bắt đầu
    if not st.session_state.quiz_state["started"]:
        # Hiển thị thông báo chỉ 1 lần
        if "name_prompt_shown" not in st.session_state:
            text_to_speech("Bạn tên gì")
            st.session_state.name_prompt_shown = True

        # Nút nhập tên bằng giọng nói (đặt bên ngoài form)
        if st.button("🎤 Giọng nói", key="voice_name_btn"):
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
        if st.button(f"🎤 Giọng nói"):
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