from text_to_speech.authenticator import Authenticator
from text_to_speech.text_to_speech_service import TextToSpeechService
from text_to_speech.audio_handler import AudioHandler
from text_to_speech.app import TextToSpeechApp
from text_to_speech.config import API_TOKEN, URL, PROVIDERS, LANGUAGE, OPTION, FALLBACK_PROVIDERS
from text_configuration.main import response_sentences_for_speech

# Instantiate and run the application
authenticator = Authenticator(API_TOKEN)
tts_service = TextToSpeechService(URL, PROVIDERS, LANGUAGE, OPTION, FALLBACK_PROVIDERS)
audio_handler = AudioHandler()

app = TextToSpeechApp(authenticator, tts_service, audio_handler)
app.run(response_sentences_for_speech)
