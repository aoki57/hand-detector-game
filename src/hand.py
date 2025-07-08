# hand.py
import pygame

class Hand:
    def __init__(self, image_path, screen):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.screen = screen
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (60, 120))

    def update(self):
        pos = pygame.mouse.get_pos()
        
        # Offset untuk geser gambar agar telapak tangan sejajar kursor
        offset_x = 165
        offset_y = 330  # Geser ke atas, sesuaikan nilai sampai pas

        self.rect.centerx = pos[0] + offset_x
        self.rect.centery = pos[1] + offset_y

        self.screen.blit(self.image, self.rect)