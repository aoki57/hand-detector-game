# game.py
import pygame
import sys
import cv2
import threading
from settings import *
from insect import Insect
from hand import Hand
from hand_tracking import HandDetector

# Global var untuk posisi tangan
hand_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# OpenCV + Mediapipe Setup
cap = cv2.VideoCapture(0)
detector = HandDetector()

def run_camera():
    global hand_position
    while True:
        success, img = cap.read()
        if not success:
            continue
        img = cv2.flip(img, 1)  # mirror
        img, hands = detector.find_hands(img)

        if hands:
            x, y = hands[0][9]  # landmark 9 = titik tengah telapak tangan
            hand_position = (x, y)

        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Mulai thread webcam
camera_thread = threading.Thread(target=run_camera)
camera_thread.daemon = True
camera_thread.start()

def game():
    pygame.init()
    pygame.display.set_caption("Hand Mosquito Game")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    hand = Hand("assets/img/hand.png", screen)
    background = pygame.image.load("assets/img/background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    mosquitos = [Insect("assets/img/mosquito.png", screen, 3, +1) for _ in range(5)]
    bees = [Insect("assets/img/bee.png", screen, 2, +1) for _ in range(5)]

    score = 0
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    while True:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
                sys.exit()

        for m in mosquitos:
            m.update()
        for b in bees:
            b.update()

        # Update posisi tangan berdasarkan webcam
        hand.update(hand_position)

        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

        pygame.display.update()
        clock.tick(60)
