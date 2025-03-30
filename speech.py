import pyttsx3
import keyboard
import requests
import pygame
import os
import time

engine = pyttsx3.init()
voices = engine.getProperty('voices')

voice_vi = None
voice_en = None

for voice in voices:
    if "An" in voice.name:
        voice_vi = voice.id
        # print(voice_vi)
        # print(voice_vi)
        # print(voice_vi)
    elif "Zira" in voice.name or "David" in voice.name:
        voice_en = voice.id

engine.setProperty('rate', 150)


def text_to_speech(text, lang="vi"):
    if lang == "vi" and voice_vi:
        engine.setProperty('voice', voice_vi)
    elif lang == "en" and voice_en:
        engine.setProperty('voice', voice_en)

    engine.say(text)
    engine.runAndWait()



def text_to_speech_v2(text, filename="output.mp3"):
    url = 'https://api.fpt.ai/hmi/tts/v5'
    headers = {
        'api-key': 'qs8SxCjCU8K09dAwa60GHCrdLagfZrlK',
        'speed': '1',
        'voice': 'linhsan'
    }

    response = requests.post(url, headers=headers, data=text.encode('utf-8'))
    response_json = response.json()

    if "async" in response_json:
        audio_url = response_json["async"]

        # Tải file về
        audio_response = requests.get(audio_url, stream=True)
        with open(filename, "wb") as f:
            for chunk in audio_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        # Đợi một chút để file hoàn thành tải xuống
        time.sleep(1)

        # Kiểm tra file có hợp lệ không
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            print("Lỗi: File tải xuống không hợp lệ!")
            return

        # Chạy âm thanh bằng pygame
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            # Chờ phát xong
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            pygame.mixer.music.stop()
        except pygame.error as e:
            print("Lỗi khi phát file:", e)

        pygame.mixer.quit()

        # Xóa file sau khi phát xong
        try:
            os.remove(filename)
        except PermissionError:
            print("Không thể xóa file, có thể vẫn đang được sử dụng!")

    else:
        print("Lỗi API:", response_json.get("message", "Không rõ nguyên nhân"))


special_keys = {
    "space": "space",
    "enter": "enter",
    "backspace": "backspace",
    "shift": "shift",
    "ctrl": "control",
    "alt": "alt",
    "tab": "tab",
    "caps lock": "caps lock",
    "esc": "escape",
    "up": "up arrow",
    "down": "down arrow",
    "left": "left arrow",
    "right": "right arrow",
    "delete": "delete",
    "home": "home",
    "end": "end",
    "page up": "page up",
    "page down": "page down"
}


def listen_keyboard():
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name.lower()

            if key in special_keys:
                text_to_speech(special_keys[key], lang="en")
            elif len(key) == 1:
                text_to_speech(key, lang="vi")
            else:
                print(f"Bỏ qua: {key}")


# listen_keyboard()
# text_to_speech("xin chào", lang="vi")
# print("alo")
# text_to_speech("xin chào", lang="vi")
# text_to_speech("xin chào", lang="vi")