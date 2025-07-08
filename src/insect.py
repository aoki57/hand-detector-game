#insect.py
import pygame
import random
from settings import *

class Insect:
    def __init__(self, image_path, screen, speed, point_value):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.screen = screen
        self.point_value = point_value

        scale = random.uniform(0.7, 1.0)
        self.image = pygame.transform.scale(
            self.image,
            (int(INSECT_SIZE*scale), int(INSECT_SIZE*scale))
        )

        if random.choice([True, False]):
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen.get_width() - self.rect.width)
        self.rect.y = random.randint(0, screen.get_height() - self.rect.height)

        self.speed_x = random.choice([-1, 1]) * speed
        self.speed_y = random.choice([-1, 1]) * speed

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= self.screen.get_width():
            self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= self.screen.get_height():
            self.speed_x *= -1
        
        self.screen.blit(self.image, self.rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)