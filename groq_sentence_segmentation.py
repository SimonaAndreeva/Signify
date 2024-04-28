import os
from groq import Groq
from words_segmentation import segmented_words
from groq_api_key import api_key

client = Groq(api_key=api_key)

# Join segmented words into a single string
word_segmented = ' '.join(segmented_words)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"Take this words: {word_segmented} and put the right punctuation so they become sentences. You must not inlcude explanation!",
        }
    ],
    model="mixtral-8x7b-32768",
)

response = chat_completion.choices[0].message.content

print(response)
