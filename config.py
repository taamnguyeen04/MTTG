
import json
import os
import pygame
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from gtts import gTTS
import speech_recognition as sr
import streamlit as st

# Đường dẫn file
LESSONS_FILE = "data/lessons.json"
QUESTIONS_FILE = "data/questions.json"
RESULTS_FILE = "results.json"
FLASHCARDS_FILE = "data/flashcards.json"
os.makedirs("data", exist_ok=True)

# Khởi tạo pygame mixer
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
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except PermissionError:
                return False
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
        return r.recognize_google(audio, language="vi-VI")
    except sr.UnknownValueError:
        return "Không nhận diện được giọng nói."
    except sr.RequestError:
        return "Lỗi kết nối đến dịch vụ nhận diện giọng nói."
