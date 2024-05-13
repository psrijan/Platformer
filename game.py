import pygame
from player import Soldier, Bullet
import time
from enemy import Enemy

PLAYER_SPEED = 15

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
GAME_LOOP_RUNNING = True
player = Soldier(700, 300, .25)
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

FPS = 100

clock.tick(FPS)

# bullet group to hold the bullets created by the user
bullet_group = pygame.sprite.Group()

while GAME_LOOP_RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_LOOP_RUNNING = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            elif event.key == pygame.K_d:
                move_right = True

            if event.key == pygame.K_w:
                jump = True

            if event.key == pygame.K_LSHIFT:
                aim = True
            elif event.key == pygame.K_SPACE:
                shoot = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
                move_right = False # remove this later
            elif event.key == pygame.K_d:
                move_right = False
                move_left = False # remove this later

            if event.key == pygame.K_w:
                jump = False

            if event.key == pygame.K_LSHIFT:
                aim = False
            if event.key == pygame.K_SPACE:
                shoot = False

        if move_left or move_right:
            player.update_player_action(RUN)
        elif shoot:
            player.update_player_action(SHOOT)
        elif aim:
            player.update_player_action(AIM)
        else:
            player.update_player_action(IDLE)

    if shoot:
        player.shoot(bullet_group)
        # players direction will be -1 or +1 depending on which way he is looking
        # print("PLAYERS ")
        # bullet = Bullet(player.rect.centerx + (player.rect.width * .6 * player.direction),
        #                 player.rect.centery, player.direction)
        # bullet_group.add(bullet)

    for bullet in bullet_group.sprites():
        bullet.add_hit_strikes(player, enemy1, bullet_group)

    bullet_group.update()



    player.move(move_left, move_right, jump, PLAYER_SPEED)
    enemy.move()
    enemy1.move()
    enemy1.update()

    screen.fill((0, 0, 0))
    player.draw(screen)
    # enemy.draw(screen)
    enemy1.draw(screen)
    bullet_group.draw(screen)

    player.detect_collission(enemy1.rect)

    # player.move(move_left, move_right, 5)

    # pygame.draw.rect(screen, pygame.Color(100,100,100, 100), pygame.rect.Rect(100, 100, 100, 100))
    pygame.display.flip()
    pygame.time.delay(150) # @todo check if this is a way to delay frame rate in python.

pygame.quit()