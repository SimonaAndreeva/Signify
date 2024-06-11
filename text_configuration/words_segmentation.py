# Importing the wordsegment module
import wordsegment

# Importing letters_array from the data_training.interface_classifier module
from app import get_letters_array

# Loading the wordsegment module's data
wordsegment.load()

# Joining the list of letters (letters_array) into a single string
letters_string = ''.join(get_letters_array())

# Segmenting the combined string into words
segmented_words = wordsegment.segment(letters_string)
