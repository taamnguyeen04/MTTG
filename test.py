import cv2
import pyautogui
import keyboard
import numpy as np
import time
import pygame

# Khởi tạo pygame mixer
pygame.mixer.init()

def play_sound(sound_path):
    try:
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        time.sleep(2)  # Đợi 2 giây
        pygame.mixer.music.stop()  # Dừng phát nhạc
    except Exception as e:
        print(f"Lỗi phát âm thanh: {e}")
    pygame.mixer.music.stop()

def find_and_click(image_path, threshold=0.8):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"Không tìm thấy ảnh: {image_path}")
        return False

    h, w = template.shape[:2]
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        pyautogui.moveTo(center_x, center_y, duration=0.2)
        pyautogui.click()
        return True
    return False

print("Giữ Shift và nhấn 1/2/3/4 để click ảnh. Giữ Shift và nhấn e/v/j để phát âm thanh.")

try:
    while True:
        if keyboard.is_pressed('alt'):
            if keyboard.is_pressed('1'): # về trang chủ
                print("Alt + 1 được nhấn")
                find_and_click('img/1.png')
                time.sleep(1)

            elif keyboard.is_pressed('2'): # tới trang bài học
                print("Alt + 2 được nhấn")
                find_and_click('img/2.png')
                time.sleep(1)

            elif keyboard.is_pressed('3'): # tới trang kiểm tra kiến thức
                print("Alt + 3 được nhấn")
                find_and_click('img/3.png')
                time.sleep(1)

            elif keyboard.is_pressed('4'): # tới trang hỗ trợ
                print("Alt + 4 được nhấn")
                find_and_click('img/4.png')
                time.sleep(1)

            elif keyboard.is_pressed('m'): # chuyển flascard tiếp theo
                print("Alt + m được nhấn")
                find_and_click('img/5.png')
                time.sleep(1)

            elif keyboard.is_pressed('5'): # bật giọng nói
                print("Alt + 5 được nhấn")
                find_and_click('img/6.png')
                time.sleep(1)

            elif keyboard.is_pressed('b'): # phát file tiếng anh flascard
                print("Alt + E được nhấn")
                play_sound('e.mp3')
                time.sleep(1)

            elif keyboard.is_pressed('v'): # phát file tiếng việt flascard
                print("Alt + V được nhấn")
                play_sound('v.mp3')
                time.sleep(1)

            elif keyboard.is_pressed('n'): # phát file tiếng nhật flascard
                print("Alt + J được nhấn")
                play_sound('j.mp3')
                time.sleep(1)

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Kết thúc chương trình.")
