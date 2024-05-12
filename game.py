import pygame
from player import Soldier
import time
from enemy import Enemy

PLAYER_SPEED = 15

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
GAME_LOOP_RUNNING = True

player = Soldier(300, 300, .25)
enemy = Enemy(300, 400, 1, 'FLYING')
enemy1 = Enemy(500, 300, 1)

move_left = False
move_right = False
jump = False
shoot = False
aim = False

IDLE = 'idle'
RUN = 'run'
SHOOT = 'shoot'
AIM = 'aim'

while GAME_LOOP_RUNNING:
    print('running')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_LOOP_RUNNING = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print('A clicked')
                move_left = True
            elif event.key == pygame.K_d:
                print('D clicked')
                move_right = True

            if event.key == pygame.K_w:
                print('w clicked')
                jump = True

            if event.key == pygame.K_LSHIFT:
                print('aiming - LSHIFT pressed')
                aim = True
            elif event.key == pygame.K_SPACE:
                print('shoot')
                shoot = True
                print('space pressed shooting now')

        if event.type == pygame.KEYUP:
            print('key up event triggered')
            if event.key == pygame.K_a:
                print('A released')
                move_left = False
                move_right = False # remove this later
            elif event.key == pygame.K_d:
                print('D released')
                move_right = False
                move_left = False # remove this later

            if event.key == pygame.K_w:
                jump = False
                print('w released')

            if event.key == pygame.K_LSHIFT:
                aim = False
                print('aiming removed')
            if event.key == pygame.K_SPACE:
                shoot = False
                print('space released not shooting')


        print(f'move_left: {move_left} -- move_right: {move_right}')

        if move_left or move_right:
            player.update_player_action(RUN)
        elif shoot:
            player.update_player_action(SHOOT)
        elif aim:
            player.update_player_action(AIM)
        else:
            player.update_player_action(IDLE)

    player.move(move_left, move_right, jump, PLAYER_SPEED)
    enemy.move()
    enemy1.move()

    screen.fill((0, 0, 0))
    player.draw(screen)
    enemy.draw(screen)
    enemy1.draw(screen)

    # player.move(move_left, move_right, 5)

    # pygame.draw.rect(screen, pygame.Color(100,100,100, 100), pygame.rect.Rect(100, 100, 100, 100))
    pygame.display.flip()
    pygame.time.delay(200) # @todo check if this is a way to delay frame rate in python.

pygame.quit()