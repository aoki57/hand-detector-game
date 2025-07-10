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
last_camera_frame = None  # ⬅️ Tambahkan ini di atas

# OpenCV + Mediapipe Setup
cap = cv2.VideoCapture(0)
detector = HandDetector()

is_fist = False

def run_camera():
    cam_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    global hand_position, last_camera_frame, is_fist
    while True:
        success, img = cap.read()
        if not success:
            continue
        img = cv2.flip(img, 1)  # mirror
        img, hands = detector.find_hands(img)

        if hands:
            x, y = hands[0][9]  # landmark 9 = titik tengah telapak tangan
            screen_x, screen_y = convert_to_screen_coords(x, y, cam_width, cam_height)
            hand_position = (screen_x, screen_y)

            finger_count = detector.count_fingers(hands[0])
            is_fist = finger_count == 0  # tangan menggempal jika semua jari tertutup
        else:
            is_fist = False

        last_camera_frame = img.copy()  # Simpan hasil akhir frame

        # cv2.imshow("Webcam", img)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

# Mulai thread webcam
camera_thread = threading.Thread(target=run_camera)
camera_thread.daemon = True
camera_thread.start()

def game():
    pygame.init()
    pygame.display.set_caption("Hand Mosquito Game")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def reset_game():
        return (
            Hand("assets/img/hand.png", screen),
            [Insect("assets/img/mosquito.png", screen, 3, +1) for _ in range(5)],
            [Insect("assets/img/bee.png", screen, 2, +1) for _ in range(5)],
            0,  # skor
            False  # game_over
        )

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Tombol untuk UI Game Over
    button_restart = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 40)
    button_quit = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 40)

    hand, mosquitos, bees, score, game_over = reset_game()

    background = pygame.image.load("assets/img/background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    while running:
        screen.blit(background, (0, 0))

        if last_camera_frame is not None:
            frame = cv2.cvtColor(last_camera_frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (160, 120))
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame_surface, (SCREEN_WIDTH - 160 - 10, SCREEN_HEIGHT - 120 - 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if button_restart.collidepoint(event.pos):
                    hand, mosquitos, bees, score, game_over = reset_game()
                elif button_quit.collidepoint(event.pos):
                    running = False

        # Jalankan game hanya jika belum selesai
        if not game_over:
            for m in mosquitos:
                m.update()
            for b in bees:
                b.update()

            # Update posisi tangan dari webcam
            hand.update(hand_position, is_fist)

            # Deteksi tabrakan hanya jika tangan menggempal
            if is_fist:
                for m in mosquitos[:]:
                    if hand.rect.colliderect(m.rect):
                        mosquitos.remove(m)
                        score += 1
                for b in bees[:]:
                    if hand.rect.colliderect(b.rect):
                        bees.remove(b)
                        score -= 1

                # Semua nyamuk habis? Game selesai
                if not mosquitos:
                    game_over = True

        else:
            # UI Game Over
            game_over_surface = font.render("Semua nyamuk telah dibasmi!", True, (255, 255, 0))
            score_surface = font.render(f"Skor Akhir: {score}", True, (255, 255, 255))
            screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 70))
            screen.blit(score_surface, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))

            # Tombol Ulangi
            pygame.draw.rect(screen, (0, 128, 0), button_restart)
            restart_text = font.render("Ulangi", True, (255, 255, 255))
            screen.blit(restart_text, (button_restart.x + 60, button_restart.y + 5))

            # Tombol Keluar
            pygame.draw.rect(screen, (128, 0, 0), button_quit)
            quit_text = font.render("Keluar", True, (255, 255, 255))
            screen.blit(quit_text, (button_quit.x + 65, button_quit.y + 5))

        # Tampilkan skor (selalu tampil)
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

        pygame.display.update()
        clock.tick(60)

    # Setelah keluar dari game
    pygame.quit()
    cap.release()
    # cv2.destroyAllWindows()

def convert_to_screen_coords(x, y, cam_width, cam_height):
    screen_x = int(x / cam_width * SCREEN_WIDTH)
    screen_y = int(y / cam_height * SCREEN_HEIGHT)
    return screen_x, screen_y

