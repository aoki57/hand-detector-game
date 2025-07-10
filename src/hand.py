# hand.py
import pygame

class Hand:
    def __init__(self, image_path, screen):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.screen = screen

        self.image_normal = pygame.transform.scale(self.original_image, (60, 120))
        self.image_fist = pygame.transform.scale(self.original_image, (50, 100))
        self.rect = self.image_normal.get_rect()

    def update(self, hand_position=None, is_fist=False):
        if hand_position is not None:
            pos = hand_position
        else:
            pos = pygame.mouse.get_pos()

        offset_x = -30
        offset_y = -30

        image_to_draw = self.image_fist if is_fist else self.image_normal
        self.rect = image_to_draw.get_rect()
        self.rect.centerx = pos[0] + offset_x
        self.rect.centery = pos[1] + offset_y

        self.screen.blit(image_to_draw, self.rect)

