from gtts import gTTS
import pygame
import keyboard
import os

# Từ điển ánh xạ phím đặc biệt sang tiếng Việt
special_keys = {
    'space': 'Phím cách',
    'enter': 'Phím enter',
    'backspace': 'Phím xóa lùi',
    'tab': 'Phím tab',
    'esc': 'Phím escape',
    'delete': 'Phím xóa',
    'up': 'Phím mũi tên lên',
    'down': 'Phím mũi tên xuống',
    'left': 'Phím mũi tên trái',
    'right': 'Phím mũi tên phải',
    'home': 'Phím home',
    'end': 'Phím end',
    'page up': 'Phím page up',
    'page down': 'Phím page down',
    'caps lock': 'Phím caps lock',
    'shift': 'Phím shift',
    'ctrl': 'Phím control',
    'alt': 'Phím alt',
    'windows': 'Phím windows',
    'menu': 'Phím menu',
    'num lock': 'Phím num lock'
}

# Thêm các phím F1-F12
for i in range(1, 13):
    special_keys[f'f{i}'] = f'Phím F {i}'


# Danh sách tổ hợp cần bỏ qua
ignored_combinations = {
    'alt+1', 'alt+2', 'alt+3', 'alt+4',
    'alt+v', 'alt+b', 'alt+n', 'alt+m'
}


def text_to_speech(text, filename="output.mp3"):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except PermissionError:
            print("Lỗi: Không thể xóa tệp cũ!")
            return

    try:
        tts = gTTS(text=text, lang='vi', slow=False)
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        pygame.mixer.quit()


def listen_keyboard():
    typed_text = ""
    combo = []

    def speak_key(key):
        # Bỏ qua nếu key nằm trong danh sách bị loại trừ
        if key.lower() in ignored_combinations:
            print(f"Đã bỏ qua tổ hợp: {key}")
            return

        # Xử lý phím đặc biệt
        if key in special_keys:
            text_to_speech(special_keys[key])
        # Xử lý tổ hợp phím
        elif '+' in key:
            keys = key.split('+')
            text = ' '.join([special_keys.get(k, k) for k in keys])
            text_to_speech(f'Tổ hợp {text}')
        # Xử lý ký tự thường
        else:
            text_to_speech(f'{key}')

    def handle_key(event):
        nonlocal typed_text, combo

        if event.event_type == keyboard.KEY_DOWN:
            key = event.name

            # Bỏ qua các phím modifier khi đứng riêng
            if key in ['shift', 'ctrl', 'alt', 'windows']:
                combo.append(key)
                return

            # Xử lý tổ hợp phím
            if combo:
                key_combination = '+'.join(combo + [key])
                speak_key(key_combination)
                combo = []
            else:
                # Xử lý phím đơn
                if key == 'space':
                    if typed_text:
                        text_to_speech(typed_text)
                    typed_text = ""
                elif key == 'backspace':
                    typed_text = typed_text[:-1]
                    text_to_speech("Đã xóa")
                elif key == 'enter':
                    text_to_speech("Đã xuống dòng")
                else:
                    typed_text += key
                    speak_key(key)

    keyboard.hook(handle_key)
    keyboard.wait()


# Chạy chương trình
text_to_speech("Chương trình đọc phím tiếng Việt đã sẵn sàng", "ready.mp3")
listen_keyboard()
