import streamlit as st
import json
import pandas as pd
from datetime import datetime
import os

# Cấu hình trang
st.set_page_config(
    page_title="Hệ thống Quản lý Quiz Python",
    page_icon="👨‍🏫",
    layout="wide",
    menu_items={
        'Get Help': 'https://github.com/streamlit',
        'Report a bug': "https://github.com/streamlit",
        'About': "Hệ thống quản lý Quiz Python - Phiên bản 1.0"
    }
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .teacher-header {
        font-size: 28px;
        color: #3a7bd5;
        padding-bottom: 10px;
        border-bottom: 2px solid #3a7bd5;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .question-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .lesson-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
    }
    .activity-item {
        background-color: #f8f9fa;
        border-left: 4px solid #3a7bd5;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 0 5px 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# Đường dẫn file
QUESTIONS_FILE = "data/test.json"
RESULTS_FILE = "results.json"
LESSONS_FILE = "data/lessons.json"


# ========== CÁC HÀM CHỨC NĂNG ==========

def load_questions():
    """Tải danh sách câu hỏi từ file"""
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_questions(questions):
    """Lưu danh sách câu hỏi vào file"""
    os.makedirs(os.path.dirname(QUESTIONS_FILE), exist_ok=True)
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)


def load_results():
    """Tải kết quả học sinh từ file"""
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_lessons():
    """Tải danh sách bài học từ file"""
    try:
        with open(LESSONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_lessons(lessons):
    """Lưu danh sách bài học vào file"""
    os.makedirs(os.path.dirname(LESSONS_FILE), exist_ok=True)
    with open(LESSONS_FILE, "w", encoding="utf-8") as f:
        json.dump(lessons, f, indent=4, ensure_ascii=False)


# ========== GIAO DIỆN XEM KẾT QUẢ ==========

def show_results():
    """Hiển thị kết quả học sinh"""
    st.markdown("<div class='teacher-header'>📊 Kết quả học sinh</div>", unsafe_allow_html=True)

    results = load_results()

    if not results:
        st.warning("Chưa có dữ liệu kết quả nào được ghi lại.")
        return

    # Chuyển đổi sang DataFrame
    df = pd.DataFrame(results)

    # Thống kê cơ bản
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='metric-box'>"
                    f"<h3>Tổng số bài làm</h3>"
                    f"<h1>{len(df)}</h1>"
                    "</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-box'>"
                    f"<h3>Điểm cao nhất</h3>"
                    f"<h1>{df['score'].max()}</h1>"
                    "</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-box'>"
                    f"<h3>Điểm trung bình</h3>"
                    f"<h1>{df['score'].mean():.1f}</h1>"
                    "</div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-box'>"
                    f"<h3>Điểm thấp nhất</h3>"
                    f"<h1>{df['score'].min()}</h1>"
                    "</div>", unsafe_allow_html=True)

    # Bảng xếp hạng
    st.subheader("Bảng xếp hạng chi tiết")
    df_sorted = df.sort_values("score", ascending=False).reset_index(drop=True)
    df_sorted.index = df_sorted.index + 1
    st.dataframe(df_sorted, use_container_width=True)

    # Phân tích dữ liệu
    st.subheader("Phân tích kết quả")

    tab1, tab2 = st.tabs(["Phân phối điểm số", "Xu hướng theo thời gian"])

    with tab1:
        st.bar_chart(df["score"].value_counts().sort_index())

    with tab2:
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df.set_index("timestamp", inplace=True)
            st.line_chart(df["score"].resample("D").count())
        else:
            st.warning("Không có dữ liệu thời gian")

    # Xuất dữ liệu
    st.subheader("Xuất dữ liệu")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Tải xuống toàn bộ kết quả (CSV)",
        data=csv,
        file_name=f"ket_qua_quiz_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


# ========== GIAO DIỆN SOẠN CÂU HỎI ==========

def create_question():
    """Giao diện tạo câu hỏi mới"""
    st.markdown("<div class='teacher-header'>✏️ Soạn câu hỏi mới</div>", unsafe_allow_html=True)

    with st.form("question_form", clear_on_submit=True):
        question = st.text_area("Nội dung câu hỏi:", height=100, placeholder="Nhập nội dung câu hỏi...")

        col1, col2 = st.columns(2)
        with col1:
            option_a = st.text_input("Đáp án A:", placeholder="Nhập đáp án A")
            option_b = st.text_input("Đáp án B:", placeholder="Nhập đáp án B")
        with col2:
            option_c = st.text_input("Đáp án C:", placeholder="Nhập đáp án C")
            option_d = st.text_input("Đáp án D:", placeholder="Nhập đáp án D")

        correct_answer = st.selectbox("Đáp án đúng:", ["A", "B", "C", "D"])
        topic = st.text_input("Chủ đề:", placeholder="Ví dụ: Toán, Đạo đức, Anh văn...")
        difficulty = st.slider("Độ khó:", 1, 5, 3)

        submitted = st.form_submit_button("Lưu câu hỏi")

        if submitted:
            if not question or not all([option_a, option_b, option_c, option_d]):
                st.error("Vui lòng điền đầy đủ nội dung câu hỏi và các đáp án!")
            else:
                new_question = {
                    "cau_hoi": question,
                    "dap_an": [option_a, option_b, option_c, option_d],
                    "dap_an_dung": correct_answer,
                    "chu_de": topic if topic else "Khác",
                    "do_kho": difficulty
                }

                questions = load_questions()
                questions.append(new_question)
                save_questions(questions)

                st.success("✅ Câu hỏi đã được lưu thành công!")
                st.balloons()


# ========== QUẢN LÝ NGÂN HÀNG CÂU HỎI ==========

def manage_questions():
    """Giao diện quản lý câu hỏi"""
    st.markdown("<div class='teacher-header'>📝 Quản lý ngân hàng câu hỏi</div>", unsafe_allow_html=True)

    questions = load_questions()

    if not questions:
        st.info("Ngân hàng câu hỏi trống.")
        return

    # Bộ lọc và tìm kiếm
    col1, col2 = st.columns(2)
    with col1:
        topics = ["Tất cả"] + sorted(list(set(q.get("chu_de", "Khác") for q in questions)))
        selected_topic = st.selectbox("Lọc theo chủ đề:", topics)
    with col2:
        search_term = st.text_input("Tìm kiếm câu hỏi:")

    # Áp dụng bộ lọc
    filtered_questions = questions
    if selected_topic != "Tất cả":
        filtered_questions = [q for q in filtered_questions if q.get("chu_de", "Khác") == selected_topic]
    if search_term:
        filtered_questions = [q for q in filtered_questions if search_term.lower() in q["cau_hoi"].lower()]

    # Hiển thị thống kê
    st.info(f"Đang hiển thị {len(filtered_questions)}/{len(questions)} câu hỏi")

    # Hiển thị từng câu hỏi
    for i, q in enumerate(filtered_questions):
        with st.expander(f"Câu {i + 1}: {q['cau_hoi']} (Độ khó: {'⭐' * q.get('do_kho', 3)})", expanded=False):
            st.markdown(f"**Chủ đề:** {q.get('chu_de', 'Không xác định')}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**A.** {q['dap_an'][0]}")
                st.markdown(f"**B.** {q['dap_an'][1]}")
            with col2:
                st.markdown(f"**C.** {q['dap_an'][2]}")
                st.markdown(f"**D.** {q['dap_an'][3]}")

            st.success(f"Đáp án đúng: {q['dap_an_dung']}")

            # Nút chỉnh sửa và xóa
            col1, col2, _ = st.columns([1, 1, 2])
            with col1:
                if st.button(f"✏️ Sửa", key=f"edit_{i}"):
                    st.session_state.edit_index = i
                    st.session_state.edit_question = q
                    st.rerun()
            with col2:
                if st.button(f"🗑️ Xóa", key=f"delete_{i}"):
                    questions.remove(q)
                    save_questions(questions)
                    st.success("Đã xóa câu hỏi!")
                    st.rerun()


# ========== GIAO DIỆN CHỈNH SỬA CÂU HỎI ==========

def edit_question():
    """Giao diện chỉnh sửa câu hỏi"""
    st.markdown("<div class='teacher-header'>✏️ Chỉnh sửa câu hỏi</div>", unsafe_allow_html=True)

    if "edit_question" not in st.session_state:
        st.warning("Không có câu hỏi nào được chọn để chỉnh sửa")
        st.button("Quay lại", on_click=lambda: st.session_state.pop("edit_index"))
        return

    q = st.session_state.edit_question
    index = st.session_state.edit_index

    with st.form("edit_form"):
        question = st.text_area("Nội dung câu hỏi:", value=q["cau_hoi"], height=100)

        col1, col2 = st.columns(2)
        with col1:
            option_a = st.text_input("Đáp án A:", value=q["dap_an"][0])
            option_b = st.text_input("Đáp án B:", value=q["dap_an"][1])
        with col2:
            option_c = st.text_input("Đáp án C:", value=q["dap_an"][2])
            option_d = st.text_input("Đáp án D:", value=q["dap_an"][3])

        correct_answer = st.selectbox("Đáp án đúng:", ["A", "B", "C", "D"],
                                      index=["A", "B", "C", "D"].index(q["dap_an_dung"]))
        topic = st.text_input("Chủ đề:", value=q.get("chu_de", ""))
        difficulty = st.slider("Độ khó:", 1, 5, q.get("do_kho", 3))

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Lưu thay đổi")
        with col2:
            cancel = st.form_submit_button("Hủy bỏ")

        if cancel:
            st.session_state.pop("edit_index")
            st.session_state.pop("edit_question")
            st.rerun()

        if submitted:
            if not question or not all([option_a, option_b, option_c, option_d]):
                st.error("Vui lòng điền đầy đủ nội dung câu hỏi và các đáp án!")
            else:
                questions = load_questions()
                questions[index] = {
                    "cau_hoi": question,
                    "dap_an": [option_a, option_b, option_c, option_d],
                    "dap_an_dung": correct_answer,
                    "chu_de": topic if topic else "Khác",
                    "do_kho": difficulty
                }
                save_questions(questions)

                st.success("✅ Câu hỏi đã được cập nhật thành công!")
                st.session_state.pop("edit_index")
                st.session_state.pop("edit_question")
                st.balloons()
                st.rerun()


# ========== GIAO DIỆN SOẠN BÀI HỌC ==========

def create_lesson():
    """Giao diện tạo bài học mới"""
    st.markdown("<div class='teacher-header'>📖 Soạn bài học mới</div>", unsafe_allow_html=True)

    with st.form("lesson_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            subject = st.text_input("Môn học:", placeholder="Ví dụ: Đạo đức, Toán, Tiếng Việt...")
        with col2:
            lesson_title = st.text_input("Tên bài học:", placeholder="Ví dụ: Biết ơn người lao động...")

        description = st.text_area("Mô tả ngắn:", height=80,
                                   placeholder="Mô tả ngắn gọn về bài học...")

        st.markdown("**Nội dung bài học:**")
        content_text = st.text_area("Nội dung văn bản:", height=150,
                                    placeholder="Nhập nội dung chi tiết bài học...")

        content_audio = st.text_area("Nội dung audio (ghi chú cho file âm thanh):", height=100,
                                     placeholder="Ghi chú nội dung cho file âm thanh (nếu có)...")

        image_file = st.text_input("Đường dẫn hình ảnh:", placeholder="Ví dụ: img/lao_cong.png")

        # Phần hoạt động
        st.markdown("**Hoạt động bài học:**")
        activities = st.session_state.get("activities", [])

        for i, activity in enumerate(activities):
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"<div class='activity-item'>"
                                f"<b>{activity['ten_hoat_dong']}</b><br>"
                                f"{activity['noi_dung']}</div>",
                                unsafe_allow_html=True)
                with col2:
                    if st.button(f"Xóa", key=f"del_act_{i}"):
                        activities.pop(i)
                        st.session_state.activities = activities
                        st.rerun()

        with st.expander("Thêm hoạt động mới", expanded=False):
            act_name = st.text_input("Tên hoạt động:", key="act_name",
                                     placeholder="Ví dụ: Khởi động, Khám phá, Luyện tập...")
            act_content = st.text_area("Nội dung hoạt động:", key="act_content",
                                       height=100, placeholder="Mô tả chi tiết hoạt động...")
            if st.form_submit_button("Thêm hoạt động"):
                if act_name and act_content:
                    if "activities" not in st.session_state:
                        st.session_state.activities = []
                    st.session_state.activities.append({
                        "ten_hoat_dong": act_name,
                        "noi_dung": act_content
                    })
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập đủ tên và nội dung hoạt động")

        submitted = st.form_submit_button("Lưu bài học")
        if submitted:
            if not subject or not lesson_title or not content_text:
                st.error("Vui lòng điền đầy đủ thông tin môn học, tên bài và nội dung!")
            else:
                new_lesson = {
                    "mon_hoc": subject,
                    "ten_bai": lesson_title,
                    "mo_ta": description,
                    "noi_dung_text": content_text,
                    "noi_dung_audio": content_audio,
                    "hinh_anh": image_file,
                    "hoat_dong": st.session_state.get("activities", [])
                }

                lessons = load_lessons()
                lessons.append(new_lesson)
                save_lessons(lessons)

                st.success("✅ Bài học đã được lưu thành công!")
                if "activities" in st.session_state:
                    st.session_state.pop("activities")
                st.balloons()


# ========== QUẢN LÝ BÀI HỌC ==========

def manage_lessons():
    """Giao diện quản lý bài học"""
    st.markdown("<div class='teacher-header'>📚 Quản lý bài học</div>", unsafe_allow_html=True)

    lessons = load_lessons()

    if not lessons:
        st.info("Chưa có bài học nào được tạo.")
        return

    # Bộ lọc và tìm kiếm
    col1, col2 = st.columns(2)
    with col1:
        subjects = ["Tất cả"] + sorted(list(set(lesson.get("mon_hoc", "Khác") for lesson in lessons)))
        selected_subject = st.selectbox("Lọc theo môn học:", subjects)
    with col2:
        search_term = st.text_input("Tìm kiếm bài học:")

    # Áp dụng bộ lọc
    filtered_lessons = lessons
    if selected_subject != "Tất cả":
        filtered_lessons = [lesson for lesson in filtered_lessons
                            if lesson.get("mon_hoc", "Khác") == selected_subject]
    if search_term:
        filtered_lessons = [lesson for lesson in filtered_lessons
                            if search_term.lower() in lesson["ten_bai"].lower()]

    # Hiển thị thống kê
    st.info(f"Đang hiển thị {len(filtered_lessons)}/{len(lessons)} bài học")

    # Hiển thị từng bài học
    for i, lesson in enumerate(filtered_lessons):
        with st.expander(f"{lesson['mon_hoc']} - {lesson['ten_bai']}", expanded=False):
            st.markdown(f"**Mô tả:** {lesson.get('mo_ta', 'Không có mô tả')}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Nội dung văn bản:**")
                st.text(lesson.get("noi_dung_text", "Không có nội dung"))
            with col2:
                if lesson.get("hinh_anh"):
                    st.image(lesson["hinh_anh"], caption="Hình ảnh bài học", width=200)
                else:
                    st.info("Không có hình ảnh")

            st.markdown("**Hoạt động:**")
            for activity in lesson.get("hoat_dong", []):
                st.markdown(f"<div class='activity-item'>"
                            f"<b>{activity['ten_hoat_dong']}</b><br>"
                            f"{activity['noi_dung']}</div>",
                            unsafe_allow_html=True)

            # Nút chỉnh sửa và xóa
            col1, col2, _ = st.columns([1, 1, 2])
            with col1:
                if st.button(f"✏️ Sửa", key=f"edit_lesson_{i}"):
                    st.session_state.edit_lesson_index = i
                    st.session_state.edit_lesson = lesson
                    st.rerun()
            with col2:
                if st.button(f"🗑️ Xóa", key=f"delete_lesson_{i}"):
                    lessons.remove(lesson)
                    save_lessons(lessons)
                    st.success("Đã xóa bài học!")
                    st.rerun()


# ========== GIAO DIỆN CHỈNH SỬA BÀI HỌC ==========

def edit_lesson():
    """Giao diện chỉnh sửa bài học"""
    st.markdown("<div class='teacher-header'>✏️ Chỉnh sửa bài học</div>", unsafe_allow_html=True)

    if "edit_lesson" not in st.session_state:
        st.warning("Không có bài học nào được chọn để chỉnh sửa")
        st.button("Quay lại", on_click=lambda: st.session_state.pop("edit_lesson_index"))
        return

    lesson = st.session_state.edit_lesson
    index = st.session_state.edit_lesson_index

    # Khởi tạo hoạt động trong session state nếu chưa có
    if "activities" not in st.session_state:
        st.session_state.activities = lesson.get("hoat_dong", [])

    with st.form("edit_lesson_form"):
        col1, col2 = st.columns(2)
        with col1:
            subject = st.text_input("Môn học:", value=lesson.get("mon_hoc", ""))
        with col2:
            lesson_title = st.text_input("Tên bài học:", value=lesson.get("ten_bai", ""))

        description = st.text_area("Mô tả ngắn:", value=lesson.get("mo_ta", ""), height=80)

        st.markdown("**Nội dung bài học:**")
        content_text = st.text_area("Nội dung văn bản:",
                                    value=lesson.get("noi_dung_text", ""),
                                    height=150)

        content_audio = st.text_area("Nội dung audio (ghi chú cho file âm thanh):",
                                     value=lesson.get("noi_dung_audio", ""),
                                     height=100)

        image_file = st.text_input("Đường dẫn hình ảnh:",
                                   value=lesson.get("hinh_anh", ""))

        # Phần hoạt động
        st.markdown("**Hoạt động bài học:**")
        activities = st.session_state.get("activities", [])

        for i, activity in enumerate(activities):
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"<div class='activity-item'>"
                                f"<b>{activity['ten_hoat_dong']}</b><br>"
                                f"{activity['noi_dung']}</div>",
                                unsafe_allow_html=True)
                with col2:
                    if st.button(f"Xóa", key=f"del_act_edit_{i}"):
                        activities.pop(i)
                        st.session_state.activities = activities
                        st.rerun()

        with st.expander("Thêm hoạt động mới", expanded=False):
            act_name = st.text_input("Tên hoạt động:", key="act_name_edit",
                                     placeholder="Ví dụ: Khởi động, Khám phá, Luyện tập...")
            act_content = st.text_area("Nội dung hoạt động:", key="act_content_edit",
                                       height=100, placeholder="Mô tả chi tiết hoạt động...")
            if st.button("Thêm hoạt động", key="add_act_edit"):
                if act_name and act_content:
                    st.session_state.activities.append({
                        "ten_hoat_dong": act_name,
                        "noi_dung": act_content
                    })
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập đủ tên và nội dung hoạt động")

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Lưu thay đổi")
        with col2:
            cancel = st.form_submit_button("Hủy bỏ")

        if cancel:
            st.session_state.pop("edit_lesson_index")
            st.session_state.pop("edit_lesson")
            if "activities" in st.session_state:
                st.session_state.pop("activities")
            st.rerun()

        if submitted:
            if not subject or not lesson_title or not content_text:
                st.error("Vui lòng điền đầy đủ thông tin môn học, tên bài và nội dung!")
            else:
                updated_lesson = {
                    "mon_hoc": subject,
                    "ten_bai": lesson_title,
                    "mo_ta": description,
                    "noi_dung_text": content_text,
                    "noi_dung_audio": content_audio,
                    "hinh_anh": image_file,
                    "hoat_dong": st.session_state.get("activities", [])
                }

                lessons = load_lessons()
                lessons[index] = updated_lesson
                save_lessons(lessons)

                st.success("✅ Bài học đã được cập nhật thành công!")
                st.session_state.pop("edit_lesson_index")
                st.session_state.pop("edit_lesson")
                if "activities" in st.session_state:
                    st.session_state.pop("activities")
                st.balloons()
                st.rerun()


# ========== GIAO DIỆN CHÍNH ==========

def main():
    """Giao diện chính"""

    # Kiểm tra đăng nhập
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("Đăng nhập hệ thống")

        with st.form("login_form"):
            username = st.text_input("Tên đăng nhập:")
            password = st.text_input("Mật khẩu:", type="password")
            submitted = st.form_submit_button("Đăng nhập")

            if submitted:
                # Kiểm tra thông tin đăng nhập (đơn giản)
                if username == "giaovien" and password == "123456":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Tên đăng nhập hoặc mật khẩu không đúng!")
        return

    # Menu chính
    st.sidebar.title("Menu Giáo viên")
    menu_options = [
        "🏆 Xem kết quả học sinh",
        "✏️ Soạn câu hỏi mới",
        "📝 Quản lý ngân hàng câu hỏi",
        "📖 Soạn bài học mới",
        "📚 Quản lý bài học",
        "⚙️ Cài đặt hệ thống"
    ]
    choice = st.sidebar.selectbox("Chọn chức năng:", menu_options)

    # Đăng xuất
    if st.sidebar.button("🚪 Đăng xuất"):
        st.session_state.logged_in = False
        st.rerun()

    # Hiển thị giao diện tương ứng
    if choice == "🏆 Xem kết quả học sinh":
        show_results()
    elif choice == "✏️ Soạn câu hỏi mới":
        if "edit_index" in st.session_state:
            edit_question()
        else:
            create_question()
    elif choice == "📝 Quản lý ngân hàng câu hỏi":
        if "edit_index" in st.session_state:
            edit_question()
        else:
            manage_questions()
    elif choice == "📖 Soạn bài học mới":
        if "edit_lesson_index" in st.session_state:
            edit_lesson()
        else:
            create_lesson()
    elif choice == "📚 Quản lý bài học":
        if "edit_lesson_index" in st.session_state:
            edit_lesson()
        else:
            manage_lessons()
    else:
        st.markdown("<div class='teacher-header'>⚙️ Cài đặt hệ thống</div>", unsafe_allow_html=True)

        st.subheader("Import/Export dữ liệu")

        tab1, tab2 = st.tabs(["Export dữ liệu", "Import dữ liệu"])

        with tab1:
            st.write("Xuất dữ liệu ra file JSON")

            col1, col2, col3 = st.columns(3)
            with col1:
                # Export câu hỏi
                questions = load_questions()
                st.download_button(
                    label="📤 Export câu hỏi",
                    data=json.dumps(questions, indent=4, ensure_ascii=False),
                    file_name="ngan_hang_cau_hoi.json",
                    mime="application/json"
                )
            with col2:
                # Export kết quả
                results = load_results()
                st.download_button(
                    label="📤 Export kết quả",
                    data=json.dumps(results, indent=4, ensure_ascii=False),
                    file_name="ket_qua_hoc_sinh.json",
                    mime="application/json"
                )
            with col3:
                # Export bài học
                lessons = load_lessons()
                st.download_button(
                    label="📤 Export bài học",
                    data=json.dumps(lessons, indent=4, ensure_ascii=False),
                    file_name="bai_hoc.json",
                    mime="application/json"
                )

        with tab2:
            st.write("Nhập dữ liệu từ file JSON")

            upload_type = st.radio("Loại dữ liệu:", ["Câu hỏi", "Kết quả", "Bài học"])

            uploaded_file = st.file_uploader(f"Chọn file {upload_type} (JSON)", type="json")

            if uploaded_file:
                try:
                    data = json.load(uploaded_file)

                    if upload_type == "Câu hỏi":
                        save_questions(data)
                    elif upload_type == "Kết quả":
                        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=4, ensure_ascii=False)
                    else:  # Bài học
                        save_lessons(data)

                    st.success("Import dữ liệu thành công!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi khi import dữ liệu: {str(e)}")


if __name__ == "__main__":
    main()