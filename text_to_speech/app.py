class TextToSpeechApp:
    def __init__(self, authenticator, tts_service, audio_handler):
        self.authenticator = authenticator
        self.tts_service = tts_service
        self.audio_handler = audio_handler

    def run(self, text):
        headers = self.authenticator.get_headers()
        audio_response = self.tts_service.fetch_audio(text, headers)
        audio_data = self.audio_handler.decode_audio(audio_response, self.tts_service.providers)
        self.audio_handler.play_audio(audio_data)
