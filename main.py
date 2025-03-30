from alo_email import send_email
from speech import listen_keyboard
from stt import recognize_speech

text = recognize_speech()
print("Bạn đã nói:", text)

text = "Đây là nội dung email."
send_email(text)

listen_keyboard()
