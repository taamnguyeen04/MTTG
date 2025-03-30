import requests
import pygame
import keyboard

# Hàm chuyển văn bản thành giọng nói
def text_to_speech(text, filename="output.mp3"):
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

        audio_response = requests.get(audio_url, stream=True)
        with open(filename, "wb") as f:
            for chunk in audio_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print("Lỗi:", response_json.get("message", "Không rõ nguyên nhân"))

# Hàm lắng nghe bàn phím và đọc âm thanh
def listen_keyboard():
    typed_text = ""  # Lưu từ đang gõ

    while True:
        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN:  # Khi phím được nhấn xuống
            key = event.name

            if key == "space":  # Khi bấm Space -> Đọc lại từ vừa nhập
                if typed_text:
                    text_to_speech(typed_text)
                typed_text = ""

            elif key == "enter":  # Khi bấm Enter -> Đọc lại từ vừa nhập
                if typed_text:
                    text_to_speech(typed_text)
                typed_text = ""

            elif key == "backspace":  # Khi xóa ký tự
                typed_text = typed_text[:-1]

            elif len(key) == 1:  # Chỉ thêm vào nếu là ký tự bình thường
                typed_text += key
                text_to_speech(key)  # Đọc từng ký tự khi nhập

# Chạy chương trình
listen_keyboard()