import pygame
from player import Soldier
import time

PLAYER_SPEED = 15

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

player = Soldier(300, 300, .25)

move_left = False
move_right = False

IDLE = 'idle'
RUN = 'run'



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print('A clicked')
                move_left = True
            elif event.key == pygame.K_d:
                print('D clicked')
                move_right = True

        if event.type == pygame.KEYUP:
            if event.type == pygame.K_a:
                print('A released')
                move_left = False
            elif event.key == pygame.K_d:
                print('D released')
                move_right = False


        if move_left or move_right:
            player.update_player_action(RUN)
        else:
            player.update_player_action(IDLE)

        screen.fill((0, 0, 0))
        player.draw(screen)
        # player.move(move_left, move_right, 5)

        # pygame.draw.rect(screen, pygame.Color(100,100,100, 100), pygame.rect.Rect(100, 100, 100, 100))
        pygame.display.flip()

pygame.quit()