# camera_app.py
import pickle
import cv2
import mediapipe as mp
import numpy as np
import time
from collections import Counter
from threading import Thread

# Load the model
model_dict = pickle.load(open('./data_training/model.p', 'rb'))
model = model_dict['model']

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {i: chr(65 + i) for i in range(26)}  # Dictionary mapping numbers to letters

class CameraApp:
    def __init__(self):
        self.cap = None
        self.running = False
        self.thread = None
        self.shown_letters = []
        self.letters_array = []
        self.current_letter = None
        self.start_time = None

    def start_camera(self):
        if self.running:
            return

        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.thread = Thread(target=self._run)
        self.thread.start()

    def stop_camera(self):
        if not self.running:
            return

        self.running = False
        self.thread.join()
        self.cap.release()
        cv2.destroyAllWindows()

    def get_detected_letters(self):
        return self.letters_array


    

    def _run(self):
        while self.running:
            ret, frame = self.cap.read()
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

                    if self.current_letter != predicted_character:
                        self.current_letter = predicted_character
                        self.start_time = time.time()
                    elif time.time() - self.start_time >= 1:
                        self.shown_letters.append(predicted_character)
                        counted_letters = Counter(self.shown_letters)
                        most_common_letter = counted_letters.most_common(1)[0][0]
                        print("Most appeared letter within the last second:", most_common_letter)
                        self.letters_array.append(most_common_letter)
                        self.shown_letters.clear()
                        self.start_time = time.time()

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                    cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
