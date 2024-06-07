import base64  # For base64 decoding
import tempfile  # For creating temporary files
import os  # For interacting with the operating system
import playsound  # For playing audio files

class AudioHandler:
    @staticmethod
    def decode_audio(data, provider):
        """
        Decode audio data from the response JSON.

        :param data: The JSON response from the text-to-speech service.
        :param provider: The provider of the audio data.
        :return: The decoded audio data as bytes.
        """
        if provider in data and 'audio' in data[provider]:
            # Check if the provider exists in the response and if audio data is available
            return base64.b64decode(data[provider]['audio'])
        else:
            # If audio data is not found in the response, print a message and return None
            print("Audio data not found in the response.")
            return None

    @staticmethod
    def play_audio(audio_data):
        """
        Play audio data.

        :param audio_data: The audio data to be played.
        """
        if audio_data:
            # If audio data is available
            temp_audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            # Create a temporary file with a .mp3 extension
            temp_audio_file.write(audio_data)
            # Write the audio data to the temporary file
            temp_audio_file.close()
            # Close the temporary file
            playsound.playsound(temp_audio_file.name, True)
            # Play the audio file
            os.unlink(temp_audio_file.name)
            # Delete the temporary file after playing
        else:
            # If no audio data is available, print a message
            print("No audio data to play.")
