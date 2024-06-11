import requests
import json
import logging

class TextToSpeechService:
    def __init__(self, url, providers, language, option, fallback_providers):
        self.url = url
        self.providers = providers
        self.language = language
        self.option = option
        self.fallback_providers = fallback_providers

    def generate_payload(self, text):
        payload = {
            "providers": self.providers,
            "language": self.language,
            "option": self.option,
            "text": text,
            "fallback_providers": self.fallback_providers
        }
        logging.debug(f"Generated payload: {payload}")
        return payload

    def fetch_audio(self, text, headers):
        payload = self.generate_payload(text)
        logging.debug(f"Sending text to Eleven Labs: {text}")
        response = requests.post(self.url, json=payload, headers=headers)

        if response.status_code == 200:
            logging.debug(f"Received audio response: {response.json()}")
            return response.json()
        else:
            logging.error(f"Failed to get audio data. Status code: {response.status_code}")
            logging.error(f"Response body: {response.text}")
            return None
