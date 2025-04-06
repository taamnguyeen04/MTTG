import requests
import pygame
import os
#
# def text_to_speech(text, filename="output.mp3"):
#     url = 'https://api.fpt.ai/hmi/tts/v5'
#     headers = {
#         'api-key': 'qs8SxCjCU8K09dAwa60GHCrdLagfZrlK',
#         'speed': '1',
#         'voice': 'linhsan'
#     }
#
#     response = requests.post(url, headers=headers, data=text.encode('utf-8'))
#     response_json = response.json()
#
#     if "async" in response_json:
#         audio_url = response_json["async"]
#
#         audio_response = requests.get(audio_url, stream=True)
#         with open(filename, "wb") as f:
#             for chunk in audio_response.iter_content(chunk_size=1024):
#                 if chunk:
#                     f.write(chunk)
#
#         # Kiểm tra tệp sau khi tải về
#         if os.path.getsize(filename) == 0:
#             print("Lỗi: Tệp MP3 không có nội dung!")
#             return
#
#         pygame.mixer.init()
#         pygame.mixer.music.load(filename)
#         pygame.mixer.music.play()
#
#         while pygame.mixer.music.get_busy():
#             pygame.time.Clock().tick(10)
#     else:
#         print("Lỗi:", response_json.get("message", "Không rõ nguyên nhân"))
#
# text_to_speech("Xin chào, đây là giọng nói từ FPT AI")

def text_to_speech(text, filename="output.mp3"):
    url = 'https://api.fpt.ai/hmi/tts/v5'
    headers = {
        'api-key': 'qs8SxCjCU8K09dAwa60GHCrdLagfZrlK',
        'speed': '1',
        'voice': 'en_us',  # Sử dụng giọng tiếng Anh
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

        # Kiểm tra tệp sau khi tải về
        if os.path.getsize(filename) == 0:
            print("Lỗi: Tệp MP3 không có nội dung!")
            return

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print("Lỗi:", response_json.get("message", "Không rõ nguyên nhân"))

text_to_speech("Hello, this is a voice from FPT AI")