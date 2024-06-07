import requests  # For making HTTP requests
import json  # For handling JSON data

class TextToSpeechService:
    def __init__(self, url, providers, language, option, fallback_providers):
        """
        Initialize with the service URL, primary providers, language, options, and fallback providers.
        """
        self.url = url
        self.providers = providers
        self.language = language
        self.option = option
        self.fallback_providers = fallback_providers

    def generate_payload(self, text):
        """
        Create the payload for the text-to-speech request.
        """
        return {
            "providers": self.providers,
            "language": self.language,
            "option": self.option,
            "text": text,
            "fallback_providers": self.fallback_providers
        }

    def fetch_audio(self, text, headers):
        """
        Send a POST request to fetch the audio data.
        """
        payload = self.generate_payload(text)  # Generate the request payload
        response = requests.post(self.url, json=payload, headers=headers)  # Make the request
        
        if response.status_code == 200:
            # Return audio data if the request was successful
            return json.loads(response.text)
        else:
            # Print error information if the request failed
            print("Failed to get audio data. Status code:", response.status_code)
            print("Response body:", response.text)
            return None
