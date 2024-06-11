# app.py
import logging
from flask import Flask, jsonify, Response, request
from flask_cors import CORS
from data_training.interface_classifier import CameraApp
from text_to_speech.text_to_speech_service import TextToSpeechService
from text_to_speech.authenticator import Authenticator
from text_to_speech.audio_handler import AudioHandler
from text_to_speech.config import API_TOKEN, PROVIDERS, LANGUAGE, OPTION, FALLBACK_PROVIDERS, URL
from text_configuration.groq_service import GroqService

app = Flask(__name__)
CORS(app)

tts_service = TextToSpeechService(URL, PROVIDERS, LANGUAGE, OPTION, FALLBACK_PROVIDERS)
authenticator = Authenticator(API_TOKEN)
audio_handler = AudioHandler()

camera_app = CameraApp()
groq_service = GroqService()

@app.route('/api/start', methods=['POST'])
def start_camera():
    camera_app.start_camera()
    return jsonify({'status': 'Camera started'})

@app.route('/api/stop', methods=['POST'])
def stop_camera():
    camera_app.stop_camera()
    letters = camera_app.get_detected_letters()
    return jsonify({'status': 'Camera stopped', 'letters': letters})

@app.route('/video_feed')
def video_feed():
    return Response(camera_app._run(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/most_common_letter', methods=['GET'])
def get_most_common_letter():
    most_common_letter = camera_app.get_most_common_letter()
    return jsonify({'most_common_letter': most_common_letter})

@app.route('/api/letters_array', methods=['GET'])
def get_letters_array():
    letters = camera_app.get_detected_letters()
    return jsonify({'letters': letters})

@app.route('/api/process_text', methods=['POST'])
def process_text():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        processed_text = groq_service.process_text(text)
        return jsonify({'processed_text': processed_text})
    except Exception as e:
        logging.error(f"Error processing text: {e}")
        return jsonify({'error': 'Failed to process text'}), 500

@app.route('/api/text_to_speech', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    logging.debug(f"Received text for TTS: {text}")

    headers = authenticator.get_headers()
    audio_response = tts_service.fetch_audio(text, headers)
    
    if audio_response:
        logging.debug(f"Audio response: {audio_response}")
        return jsonify(audio_response), 200
    else:
        return jsonify({'error': 'Failed to fetch audio data'}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
