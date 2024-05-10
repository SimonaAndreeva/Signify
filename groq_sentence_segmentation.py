import os
from groq import Groq
import json
from words_segmentation import segmented_words
from groq_api_key import api_key

client = Groq(api_key=api_key)

# Join segmented words into a single string
word_segmented = ' '.join(segmented_words)

chat_completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "system",
            "content": "Return 'JSON'"
        },
        {
            "role": "user",
            "content": f"Take this words: {word_segmented} and put the right punctuation so they become sentences. You must not inlcude explanation!",
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
    stop=None,
)

responseSentencesJSON = chat_completion.choices[0].message.content

#print(responseSentencesJSON)

data = json.loads(responseSentencesJSON)
responseSentences = data['response']
print(responseSentences)
