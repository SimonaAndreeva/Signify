import pyttsx3
from groq_sentence_segmentation import response
engine = pyttsx3.init()
engine.say(response)
engine.runAndWait()