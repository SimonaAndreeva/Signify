import os
import pickle
import numpy as np
import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './data'

data = []
labels = []
batch_size = 10  # Number of images to process in each batch

print("Start of image processing")

for dir_ in os.listdir(DATA_DIR):
    img_paths = [os.path.join(DATA_DIR, dir_, img_path) for img_path in os.listdir(os.path.join(DATA_DIR, dir_))]

    print(f"Processing images in directory: {dir_}")  # Debug print

    for i in range(0, len(img_paths), batch_size):
        batch_img_paths = img_paths[i:i + batch_size]

        batch_data = []
        batch_labels = []

        for img_path in batch_img_paths:
            try:
                data_aux = []
                x_ = []
                y_ = []

                print(f"Processing image: {img_path}")  # Debug print

                img = cv2.imread(img_path)
                if img is None:
                    print(f"Could not read image: {img_path}")
                    continue

                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                results = hands.process(img_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y

                            x_.append(x)
                            y_.append(y)

                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                            data_aux.append(x - min(x_))
                            data_aux.append(y - min(y_))

                    while len(data_aux) < 42:
                        data_aux.append(0)  # Pad with zeros if less than 42 features

                    batch_data.append(data_aux)
                    batch_labels.append(dir_)

            except Exception as e:
                print(f"Error processing image {img_path}: {e}")

        data.extend(batch_data)
        labels.extend(batch_labels)

print("End of image processing loop")  # Debug print

# Convert data and labels to numpy arrays
data = np.array(data)
labels = np.array(labels)

print("Data conversion completed")  # Debug print

# Save data and labels to pickle file
with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

print("Data saved to pickle file")  # Debug print

print("End of script")  # Debug print
