# hand.py
import pygame

class Hand:
    def __init__(self, image_path, screen):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.screen = screen
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (60, 120))

    def update(self, hand_position=None):
        if hand_position is not None:
            pos = hand_position
        else:
            pos = pygame.mouse.get_pos()
        
        offset_x = -30  # disesuaikan agar posisi telapak tangan pas
        offset_y = -30

        self.rect.centerx = pos[0] + offset_x
        self.rect.centery = pos[1] + offset_y

        self.screen.blit(self.image, self.rect)
