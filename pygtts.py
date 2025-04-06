from gtts import gTTS
import os
import pygame


def text_to_speech(text, filename="output.mp3", language = 'en'):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except PermissionError:
            print("Lỗi: Không thể xóa tệp cũ, có thể nó đang được sử dụng!")
            return
    try:
        output = gTTS(text=text, lang=language, slow=False)
        output.save(filename)
    except Exception as e:
        print(f"Lỗi khi tạo tệp MP3: {e}")
        return
    if os.path.getsize(filename) == 0:
        print("Lỗi: Tệp MP3 không có nội dung!")
        return
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Lỗi khi phát âm thanh: {e}")
    finally:
        pygame.mixer.quit()

# text_to_speech_en("hello")
