import pyttsx3 as pytts
print("Hello wolrd")
tts_engine = pytts.init()

voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[1].id)

for voice in voices:
    print(voice)
tts_engine.say("abdul bhosdi wala hai")
tts_engine.runAndWait()

tts_engine.say("abdul bhosdi wala hai")
tts_engine.runAndWait()
