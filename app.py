import os
import shutil
from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    text = request.json.get('text')
    tts = gTTS(text=text, lang='en')
    audio = BytesIO()
    tts.write_to_fp(audio)
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
    app.run()
