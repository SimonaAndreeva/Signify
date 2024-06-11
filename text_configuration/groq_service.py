# groq_service.py
from text_configuration.config import api_key
from text_configuration.groq_client import GroqClient
from text_configuration.text_formatter import TextFormatter

class GroqService:
    def __init__(self):
        self.client = GroqClient(api_key=api_key)

    def process_text(self, text):
        word_segmented = TextFormatter.join_words(text.split())
        chat_completion = self.client.create_chat_completion(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "Return 'JSON'"
                },
                {
                    "role": "user",
                    "content": f"Take these words: {word_segmented} and put the right punctuation so they become sentences. You must not include explanation!"
                },
                {
                    "role": "user",
                    "content": "{\"response\":\"\"}"
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None
        )
        response_sentences_json = chat_completion.choices[0].message.content
        return TextFormatter.extract_response_sentences(response_sentences_json)
