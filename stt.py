# import speech_recognition as sr
#
#
# def recognize_speech():
#     """
#     Nhận diện giọng nói và chuyển đổi thành văn bản.
#     """
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Nói gì đó: ")
#         audio = r.listen(source)
#
#     try:
#         text = r.recognize_google(audio, language="vi-VI")
#         return text
#     except sr.UnknownValueError:
#         return "Không nhận diện được giọng nói."
#     except sr.RequestError:
#         return "Lỗi kết nối đến dịch vụ nhận diện giọng nói."
#
#
# if __name__ == "__main__":
#     print("Bạn nói: ", recognize_speech())

import speech_recognition as sr

r = sr.Recognizer()

# Chọn micro (thử lần lượt 1, 7, 15, 17)
device_index = 1  # Thử với 7, 15 hoặc 17 nếu không hoạt động

with sr.Microphone(device_index=device_index) as source:
    print(f"Đã chọn micro: {sr.Microphone.list_microphone_names()[device_index]} (Index: {device_index})")
    print("Nói đi (tối đa 5 giây)...")

    try:
        audio = r.listen(source, timeout=3, phrase_time_limit=5)
        print("Đã nghe xong!")

        # Nhận dạng giọng nói
        text = r.recognize_google(audio, language="vi-VN")
        print("Bạn đã nói:", text)

    except sr.WaitTimeoutError:
        print("Không nghe thấy gì! Hãy thử lại.")
    except sr.UnknownValueError:
        print("Không nhận diện được giọng nói.")
    except sr.RequestError as e:
        print(f"Lỗi kết nối API: {e}")


