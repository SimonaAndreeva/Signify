import os
import pickle
import numpy as np

print("Start of the script")

# Debug print to check if this part of the script is reached
print("Attempting to open data.pickle file")

# Check if the file exists
if os.path.exists('./data.pickle'):
    print("File exists")
else:
    print("File does not exist")
    exit()

# Debug print to check if this part of the script is reached
print("Attempting to load data from data.pickle")

# Load data from pickle file
with open('./data.pickle', 'rb') as f:
    try:
        data_dict = pickle.load(f)
        print("Data loaded successfully")
    except Exception as e:
        print(f"Error loading data: {e}")
        exit()

# Debug print to check if this part of the script is reached
print("Attempting to print data_dict keys")

# Print keys of data_dict
print("Keys in data_dict:", data_dict.keys())

# Print shape of data array and a few sample labels
print("Shape of data array:", data_dict['data'].shape)
print("Sample labels:", data_dict['labels'][:10])

print("End of the script")
