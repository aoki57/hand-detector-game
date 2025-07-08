# game.py
import pygame
import sys
from settings import *
from insect import Insect
from hand import Hand

def game():
    pygame.init()
    pygame.display.set_caption("Game")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

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
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()

                for insect in mosquitos:
                    if insect.is_clicked(click_pos):
                        score += insect.point_value
                        mosquitos.remove(insect)
                        break

                for insect in bees:
                    if insect.is_clicked(click_pos):
                        score += insect.point_value
                        bees.remove(insect)
                        break
            
        for m in mosquitos:
            m.update()
        for b in bees:
            b.update()
        
        hand.update()

        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

        pygame.display.update()
        clock.tick(60)