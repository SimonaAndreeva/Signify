import wordsegment
from interface_classifier import letters_array

wordsegment.load()
letters_string = ''.join(letters_array)
segmented_text = wordsegment.segment(letters_string)

print(segmented_text)