# groq_client.py
from groq import Groq

class GroqClient:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def create_chat_completion(self, model, messages, temperature, max_tokens, top_p, stream, response_format, stop):
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream,
            response_format=response_format,
            stop=stop
        )
