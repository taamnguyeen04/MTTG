from gtts import gTTS 
import os 

myText = "a ă â "
language = 'vi'
output = gTTS(text=myText, lang=language, slow=False)
output.save("output.mp3")
os.system("start output.mp3")
