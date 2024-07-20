import shutil
from flask import Flask, render_template, request, jsonify
import pyttsx3
from io import BytesIO
from pydub import AudioSegment
import base64
import speech_recognition as sr
import re

app = Flask(__name__)

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Set properties for the TTS engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Choose a different voice if available

rate = engine.getProperty('rate')
engine.setProperty('rate', 200)  # Adjust the rate for more natural pacing

# Define pause durations
PAUSE_COMMA = 320  # milliseconds
PAUSE_PERIOD = 240  # milliseconds
PAUSE_QUESTION = 200  # milliseconds
PAUSE_EXCLAMATION = 200  # milliseconds
PAUSE_SEMICOLON = 80  # milliseconds
PAUSE_PARAGRAPH = 1500  # milliseconds

# Function to insert pauses in text
def insert_pauses(text):
    text = re.sub(r',', f', <break time="{PAUSE_COMMA}ms"/>', text)
    text = re.sub(r'\.', f'. <break time="{PAUSE_PERIOD}ms"/>', text)
    text = re.sub(r'\?', f'? <break time="{PAUSE_QUESTION}ms"/>', text)
    text = re.sub(r'!', f'! <break time="{PAUSE_EXCLAMATION}ms"/>', text)
    text = re.sub(r';', f'; <break time="{PAUSE_SEMICOLON}ms"/>', text)
    text = re.sub(r'\n\n', f'\n\n <break time="{PAUSE_PARAGRAPH}ms"/>', text)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    text = request.json.get('text')
    audio = BytesIO()

    # Insert pauses in the text
    text_with_pauses = insert_pauses(text)

    # Save the TTS to a temporary file
    engine.save_to_file(text_with_pauses, 'temp_tts.wav')
    engine.runAndWait()

    # Convert the temporary file to BytesIO object
    with open('temp_tts.wav', 'rb') as f:
        audio.write(f.read())
    audio.seek(0)

    audio_base64 = base64.b64encode(audio.read()).decode('utf-8')
    return jsonify({"audioContent": audio_base64})

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    audio_content = request.json.get('audioContent')
    audio_data = base64.b64decode(audio_content)
    audio = BytesIO(audio_data)
    audio_segment = AudioSegment.from_file(audio)
    audio_wav = BytesIO()
    audio_segment.export(audio_wav, format='wav')
    audio_wav.seek(0)

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_wav) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return jsonify({"transcription": text})
        except sr.UnknownValueError:
            return jsonify({"error": "Google Speech Recognition could not understand audio"})
        except sr.RequestError as e:
            return jsonify({"error": f"Could not request results from Google Speech Recognition service; {e}"})

if __name__ == '__main__':
    # Check if FLAC is installed
    if not shutil.which("flac"):
        raise OSError("FLAC conversion utility not available. Please install FLAC using your operating system's package manager.")
    app.run(debug=True)
