import streamlit as st
import json
import random
import os
from gtts import gTTS
import tempfile
from pygtts import text_to_speech
#chạy chung với keyboard_lisner.py

FLASHCARDS_FILE = "data/flashcards.json"


# Load dữ liệu từ JSON
def load_flashcards():
    if os.path.exists(FLASHCARDS_FILE):
        with open(FLASHCARDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


flashcards = load_flashcards()
random.shuffle(flashcards)

# Cấu hình giao diện
st.set_page_config(page_title="Flashcard Tiếng Anh", page_icon="🃏")

# CSS để tạo hiệu ứng lật thẻ
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

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🃏 Flashcard Tiếng Anh (Lật thẻ)</h1>",
            unsafe_allow_html=True)

# Trạng thái thẻ
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.should_speak = True  # Thêm trạng thái mới để kiểm soát việc đọc từ
elif "last_index" not in st.session_state or st.session_state.last_index != st.session_state.index:
    st.session_state.should_speak = True
    st.session_state.last_index = st.session_state.index
else:
    st.session_state.should_speak = False

card = flashcards[st.session_state.index]
word = card["word"]
meaning = card["meaning"]

# Hiển thị flashcard với hiệu ứng lật
st.markdown(f"""
<div class="flashcard-container" onclick="window.location.reload();">
    <div class="flashcard">
        <div class="flashcard-front">{word.upper()}</div>
        <div class="flashcard-back">{meaning}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chỉ đọc từ khi chuyển sang thẻ mới
if st.session_state.should_speak:
    text_to_speech(word, filename="e.mp3")
    text_to_speech(meaning, filename="v.mp3", language="vi")

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