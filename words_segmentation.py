import wordsegment
from interface_classifier import letters_array

wordsegment.load()
letters_string = ''.join(letters_array)
segmented_words = wordsegment.segment(letters_string)

print(segmented_words)