import base64
import json
import requests
import tempfile
import os
import playsound
from groq_sentence_segmentation import responseSentences

# API token for authentication
headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiM2ExMzNiODMtZGJlZi00N2M5LTliMmYtYThkYjM3OWNmYzg1IiwidHlwZSI6ImFwaV90b2tlbiJ9.tj-RUU1wAXBOh2wIyXnrvNv5VwtUP2WQrpxBmA7Kn9Y"}

# API endpoint and payload
url = "https://api.edenai.run/v2/audio/text_to_speech"
payload = {
    "providers": "elevenlabs",
    "language": "en-US",
    "option": "FEMALE",
    "text": responseSentences,
    "fallback_providers": "amazon"  # Using amazon as fallback provider
}

# Print the provider used
print("Using provider:", payload["providers"])

# Make the API request
response = requests.post(url, json=payload, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response
    result = json.loads(response.text)
    
    # Check if 'elevenlabs' key is in the response
    if 'elevenlabs' in result and 'audio' in result['elevenlabs']:
        # Decode the audio data
        audio_data = base64.b64decode(result['elevenlabs']['audio'])
        
        # Save the audio data to a temporary file
        temp_audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_audio_file.write(audio_data)
        temp_audio_file.close()
        
        # Play the audio file
        playsound.playsound(temp_audio_file.name, True)
        
        # Delete the temporary audio file
        os.unlink(temp_audio_file.name)
    else:
        print("Audio data not found in the response.")
else:
    print("Failed to get audio data. Status code:", response.status_code)
    print("Response body:", response.text)
