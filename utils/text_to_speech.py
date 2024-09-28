import pyttsx3

def speak_text(text:str):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

    return True

