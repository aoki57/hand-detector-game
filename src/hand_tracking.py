# hand_tracking.py
import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_hands=1, detection_confidence=0.7):
        self.max_hands = max_hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        all_hands = []
        h, w, _ = img.shape

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                hand_points = []
                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand_points.append((cx, cy))
                
                all_hands.append(hand_points)

                if draw:
                    # Deteksi warna: hijau jika mengepal (fingers = 0), merah jika terbuka
                    finger_count = self.count_fingers(hand_points)

                    if finger_count == 0:
                        color = (0, 255, 0)  # Hijau
                    else:
                        color = (0, 0, 255)  # Merah

                    self.draw_landmarks_custom(img, hand_landmarks, color)

        return img, all_hands
    
    def count_fingers(self, hand_points):
        if len(hand_points) < 21:
            return 0  # Tidak lengkap

        fingers = []

        # Thumb: bandingkan x, karena orientasi horizontal
        if hand_points[4][0] > hand_points[3][0]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers: bandingkan y (ujung jari lebih tinggi dari sendi tengah)
        tips = [8, 12, 16, 20]
        for tip in tips:
            if hand_points[tip][1] < hand_points[tip - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)  # 0 berarti menggempal
    
    def draw_landmarks_custom(self, img, hand_landmarks, color):
        for connection in self.mp_hands.HAND_CONNECTIONS:
            start_idx = connection[0]
            end_idx = connection[1]
            x0, y0 = int(hand_landmarks.landmark[start_idx].x * img.shape[1]), int(hand_landmarks.landmark[start_idx].y * img.shape[0])
            x1, y1 = int(hand_landmarks.landmark[end_idx].x * img.shape[1]), int(hand_landmarks.landmark[end_idx].y * img.shape[0])
            cv2.line(img, (x0, y0), (x1, y1), color, 2)

        for lm in hand_landmarks.landmark:
            cx, cy = int(lm.x * img.shape[1]), int(lm.y * img.shape[0])
            cv2.circle(img, (cx, cy), 4, color, cv2.FILLED)


