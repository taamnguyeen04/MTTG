import speech_recognition as sr


def recognize_speech():
    """
    Nhận diện giọng nói và chuyển đổi thành văn bản.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Nói gì đó: ")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="vi-VI")
        return text
    except sr.UnknownValueError:
        return "Không nhận diện được giọng nói."
    except sr.RequestError:
        return "Lỗi kết nối đến dịch vụ nhận diện giọng nói."
