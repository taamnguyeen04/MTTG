import json
import os
import random
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import speech_recognition as sr
from gtts import gTTS
import pygame
import streamlit as st

LESSONS_FILE = "data/lessons.json"
QUESTIONS_FILE = "data/questions.json"
RESULTS_FILE = "results.json"
FLASHCARDS_FILE = "data/flashcards.json"
os.makedirs("data", exist_ok=True)

pygame.mixer.init()

def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def send_email(subject, body, receiver_email):
    sender_email = "tam.nguyentranminh04@hcmut.edu.vn"
    password = "toeu xjcj wgog lyav"
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
    try:
        base_name = filename
        attempt = 0
        while os.path.exists(filename):
            try:
                os.remove(filename)
                break
            except PermissionError:
                attempt += 1
                filename = f"{os.path.splitext(base_name)[0]}_{attempt}.mp3"
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
    r = sr.Recognizer()
    with sr.Microphone() as source:
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
        text_to_speech(word, filename="j.mp3", language=lang)
        text_to_speech(meaning, filename="v.mp3", language="vi")
        if romaji:
            text_to_speech(romaji, filename="e.mp3", language="en")

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