# text_formatter.py
import json

class TextFormatter:
    @staticmethod
    def join_words(words):
        return ' '.join(words)

    @staticmethod
    def extract_response_sentences(response_json):
        data = json.loads(response_json)
        return data['response']
