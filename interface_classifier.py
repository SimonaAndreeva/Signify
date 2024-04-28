import pickle
import cv2
import mediapipe as mp
import numpy as np
import time
from collections import Counter

model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
               10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
               19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}

shown_letters = []
letters_array = []
current_letter = None
start_time = None

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    frame = cv2.flip(frame, 1)

    H, W, _ = frame.shape  # Access frame.shape only when frame is not None

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        data_aux = []
        x_ = []
        y_ = []

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

        if x_ and y_:
            for i in range(len(x_)):
                data_aux.append(x_[i] - min(x_))
                data_aux.append(y_[i] - min(y_))

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            prediction = model.predict([np.asarray(data_aux)])

            predicted_character = labels_dict[int(prediction[0])]
            
            # If it's a new letter, update current_letter and start_time
            if current_letter != predicted_character:
                current_letter = predicted_character
                start_time = time.time()
            # If it's the same letter and it's been 1 second, save it
            elif time.time() - start_time >= 1:
                # Store shown letters within 1 second
                shown_letters.append(predicted_character)
                # Count occurrences of letters within 1 second
                counted_letters = Counter(shown_letters)
                # Find the most common letter
                most_common_letter = counted_letters.most_common(1)[0][0]
                print("Most appeared letter within the last second:", most_common_letter)
                letters_array.append(most_common_letter)
                # Clear shown letters for the next second
                shown_letters.clear()
                # Reset timer
                start_time = time.time()

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Shown letters:", letters_array)
