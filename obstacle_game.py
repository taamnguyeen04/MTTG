import streamlit as st
import random
import json
from PIL import Image
import speech_recognition as sr
import pygame
from gtts import gTTS
import os

# Cấu hình giao diện
st.set_page_config(page_title="Trò Chơi Vượt Qua Chướng Ngại Vật", page_icon="🏃", layout="centered")


def load_questions():
    with open("data/test.json", "r", encoding="utf-8") as f:
        return json.load(f)


def text_to_speech(text, filename="temp_speech.mp3", language='vi'):
    """Chuyển văn bản thành giọng nói và phát"""
    try:
        # Xóa file cũ nếu tồn tại
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except PermissionError:
                print("Không thể xóa file cũ")
                return False

        # Tạo file âm thanh mới
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filename)

        # Phát âm thanh
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # Chờ phát xong
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        return True
    except Exception as e:
        st.error(f"Lỗi trong text_to_speech: {str(e)}")
        return False


# CSS giao diện
st.markdown("""
<style>
    .title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        color: #388E3C;
        margin-bottom: 20px;
    }
    .track {
        font-size: 24px;
        line-height: 1.5;
        margin: 20px 0;
    }
    .question-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .question-text {
        font-size: 20px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 15px;
    }
    .answer-btn {
        width: 100%;
        padding: 12px;
        margin: 8px 0;
        font-size: 16px;
        text-align: left;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .answer-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .key-hint {
        font-size: 14px;
        color: #666;
        margin-top: 25px;
        padding: 10px;
        background-color: #e8f4f8;
        border-radius: 8px;
    }
    .score-display {
        font-size: 18px;
        font-weight: bold;
        color: #e74c3c;
        margin-bottom: 15px;
    }
    .image-container {
        margin: 15px auto;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        max-width: 100%;
        text-align: center;
    }
    .question-image {
        max-width: 100%;
        max-height: 300px;
        margin: 0 auto;
        display: block;
        border-radius: 8px;
        object-fit: contain;
        cursor: pointer;
    }
    .explanation {
        margin-top: 15px;
        padding: 10px;
        background-color: #f0f8ff;
        border-radius: 8px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Hiển thị tiêu đề
st.markdown("<p class='title'>🏃‍♂️ Trò Chơi Vượt Qua Chướng Ngại Vật 🏃‍♀️</p>", unsafe_allow_html=True)

# Khởi tạo trạng thái trò chơi
if "game_state" not in st.session_state:
    questions = load_questions()
    random.shuffle(questions)

    st.session_state.game_state = {
        "player_pos": 0,
        "current_question": 0,
        "finished": False,
        "score": 0,
        "questions": questions,
        "selected_answer": None,
        "show_result": False,
        "focused_button": 0,
        "read_question": False,
        "answer_submitted": False  # Thêm trạng thái để kiểm tra đã chọn đáp án chưa
    }


def reset_game():
    questions = load_questions()
    random.shuffle(questions)

    st.session_state.game_state = {
        "player_pos": 0,
        "current_question": 0,
        "finished": False,
        "score": 0,
        "questions": questions,
        "selected_answer": None,
        "show_result": False,
        "focused_button": 0,
        "read_question": False,
        "answer_submitted": False
    }


def check_answer(selected_option):
    game_state = st.session_state.game_state
    q = game_state["questions"][game_state["current_question"]]

    selected_char = chr(65 + selected_option)

    if selected_char == q["dap_an_dung"]:
        game_state["player_pos"] = min(10, game_state["player_pos"] + 1)
        game_state["score"] += 1
        game_state["show_result"] = True
        game_state["result_message"] = "✅ Đúng rồi! Bạn tiến lên 1 bước."
    else:
        game_state["player_pos"] = max(0, game_state["player_pos"] - 1)
        game_state["show_result"] = True
        game_state["result_message"] = f"❌ Sai rồi! Đáp án đúng là: {q['dap_an_dung']}"

    game_state["current_question"] += 1
    game_state["selected_answer"] = None
    game_state["focused_button"] = 0
    game_state["read_question"] = False
    game_state["answer_submitted"] = True  # Đánh dấu đã chọn đáp án

    if game_state["player_pos"] == 10:
        game_state["finished"] = True
        game_state["result_message"] = "🎉 Chúc mừng bạn đã về đích!"


def read_current_question():
    game_state = st.session_state.game_state
    if not game_state["finished"] and game_state["current_question"] < len(game_state["questions"]):
        q = game_state["questions"][game_state["current_question"]]
        question_text = f"Câu {game_state['current_question'] + 1}: {q['cau_hoi']}"
        options = " ".join([f"Đáp án {chr(65 + i)}: {option}." for i, option in enumerate(q['dap_an'])])
        full_text = f"{question_text} {options}"
        text_to_speech(full_text)
        game_state["read_question"] = True


def read_explanation():
    game_state = st.session_state.game_state
    if not game_state["finished"] and game_state["current_question"] < len(game_state["questions"]):
        q = game_state["questions"][game_state["current_question"]]
        if "giai_thich" in q and q["giai_thich"] and game_state["answer_submitted"]:
            text_to_speech(f"Giải thích: {q['giai_thich']}")


# JavaScript để xử lý phím tắt
keyboard_js = """
<script>
document.addEventListener('keydown', function(event) {
    if (['1','2','3','4','r','s'].includes(event.key.toLowerCase())) {
        Streamlit.setComponentValue(event.key);
    }
});
</script>
"""

key_event = st.components.v1.html(keyboard_js, height=0)

# Xử lý phím bấm
if hasattr(key_event, '_result') and key_event._result is not None:
    key = key_event._result

    if key == 'r':
        reset_game()
        st.rerun()
    elif key == 's':
        read_current_question()
        st.rerun()
    elif key in ['1', '2', '3', '4']:
        selected = int(key) - 1
        st.session_state.game_state["selected_answer"] = selected
        check_answer(selected)
        st.rerun()

# Hiển thị trò chơi
game_state = st.session_state.game_state

# Hiển thị điểm số và đường đua
st.markdown(f'<div class="score-display">Điểm số: {game_state["score"]}</div>', unsafe_allow_html=True)
line = ["🟩"] * 11
line[game_state["player_pos"]] = "🧍"
line[10] = "🏁"
st.markdown(f'<div class="track">{"".join(line)}</div>', unsafe_allow_html=True)

# Hiển thị kết quả
if game_state.get("show_result", False):
    if game_state["finished"]:
        st.success(game_state["result_message"])
    else:
        if "✅" in game_state["result_message"]:
            st.success(game_state["result_message"])
        else:
            st.error(game_state["result_message"])

# Hiển thị câu hỏi
if not game_state["finished"] and game_state["current_question"] < len(game_state["questions"]):
    q = game_state["questions"][game_state["current_question"]]

    with st.container():
        st.markdown('<div class="question-container">', unsafe_allow_html=True)

        # Hiển thị hình ảnh nếu có
        if "hinh_anh" in q and q["hinh_anh"]:
            try:
                image = Image.open(q['hinh_anh'])
                st.markdown('<div class="image-container">', unsafe_allow_html=True)

                # Tạo một nút ẩn để xử lý click vào hình ảnh
                if st.button("", key=f"image_btn_{game_state['current_question']}"):
                    read_explanation()

                st.image(image, use_container_width =True,
                         caption="Nhấn vào hình để nghe giải thích" if (
                                     "giai_thich" in q and game_state["answer_submitted"]) else "")
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Không thể tải hình ảnh: {str(e)}")

        st.markdown(f'<div class="question-text">Câu {game_state["current_question"] + 1}: {q["cau_hoi"]}</div>',
                    unsafe_allow_html=True)

        # Nút đọc câu hỏi
        if st.button("🔊 Đọc câu hỏi", key=f"read_question_{game_state['current_question']}"):
            read_current_question()

        # Hiển thị các lựa chọn
        cols = st.columns(2)
        for i, option in enumerate(q["dap_an"]):
            with cols[i % 2]:
                if st.button(
                        f"{chr(65 + i)}. {option}",
                        key=f"answer_{game_state['current_question']}_{i}",
                        on_click=check_answer,
                        args=(i,),
                        type="primary" if game_state["selected_answer"] == i else "secondary"
                ):
                    game_state["selected_answer"] = i

        # Hiển thị giải thích nếu có và đã chọn đáp án
        if "giai_thich" in q and q["giai_thich"] and game_state["answer_submitted"]:
            st.markdown(f'<div class="explanation"><b>Giải thích:</b> {q["giai_thich"]}</div>',
                        unsafe_allow_html=True)

            # Nút đọc giải thích
            if st.button("🔊 Đọc giải thích", key=f"read_explanation_{game_state['current_question']}"):
                read_explanation()

        st.markdown('</div>', unsafe_allow_html=True)

# Hiển thị khi kết thúc
elif game_state["finished"]:
    st.balloons()
    st.success(f"🏁 Bạn đã về đích với số điểm: {game_state['score']}/{len(game_state['questions'])}")
else:
    st.warning(f"⛔ Hết câu hỏi! Bạn dừng ở vị trí: {game_state['player_pos']}")

# Hướng dẫn và nút chơi lại
st.markdown("""
<div class="key-hint">
<b>Hướng dẫn:</b><br>
• Nhấn <b>1-4</b> để chọn đáp án tương ứng (1=A, 2=B, 3=C, 4=D)<br>
• Nhấn <b>S</b> để nghe đọc câu hỏi và đáp án<br>
• Nhấn <b>R</b> để chơi lại từ đầu<br>
• Nhấn vào hình ảnh để nghe giải thích (sau khi chọn đáp án)<br>
• Hoặc nhấn vào nút đáp án bằng chuột
</div>
""", unsafe_allow_html=True)

if st.button("🔄 Chơi lại", key="reset_button"):
    reset_game()
    st.rerun()