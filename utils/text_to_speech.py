from gtts import gTTS
import uuid
# Function to convert text to speech using gTTS
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    filename = f"audio_{uuid.uuid4()}.mp3"  # Generate a unique filename
    tts.save(filename)
    return filename  # Return the filename for playback