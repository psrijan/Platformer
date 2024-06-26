import pygame
from player import Soldier, Bullet, Granade
import time
from enemy import Enemy
from util import clip2, generate_bar, generate_coins
from items import ItemBox, ItemBoxType
from sounds import SoundType, SoundModule
from state import  GameState
import csv
from levels import Level


SCREEN_WIDTH = 768
SCREEN_HEIGHT = 700
ROWS = 16
COLUMNS = 150
BLOCK_PIXEL = 32 # considering each block is 32 pixel

PLAYER_SPEED = 5
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
GAME_LOOP_RUNNING = True
enemy = Enemy(300, 400, 1, 'FLYING')
enemy1 = Enemy(200, 200, 1)

move_left = False
move_right = False
jump = False
shoot = False
aim = False
granade_throw = False

IDLE = 'idle'
RUN = 'run'
SHOOT = 'shoot'
AIM = 'aim'

FPS = 60
pygame.draw.rect(screen, "green", [75, 10, 50, 20])
scroll = 1
hasGameStarted = False
state = GameState()

item_box_group = state.item_box_group
bullet_group = state.bullet_group
granade_group = state.granade_group

scroll = 0
level = Level()
level_data = level.load_level_data(0)
player = level.process_level_data(level_data, state)
sound_module = SoundModule()

while GAME_LOOP_RUNNING:
    clock.tick(FPS)
    key = pygame.key.get_pressed()
    if key[pygame.K_a] and scroll < 3000:
        scroll += 5
    if key[pygame.K_d] and scroll > 0:
        scroll -= 5

    print(f"Scroll: {scroll}")

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

            if event.key == pygame.K_x:
                granade_throw = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
                move_right = False  # remove this later
            elif event.key == pygame.K_d:
                move_right = False
                move_left = False  # remove this later

            if event.key == pygame.K_w:
                jump = False

            if event.key == pygame.K_LSHIFT:
                aim = False
            if event.key == pygame.K_SPACE:
                shoot = False

            if event.key == pygame.K_x:
                granade_throw = False

        if move_left or move_right:
            player.update(RUN)
        elif shoot:
            player.update(SHOOT)
        elif aim:
            player.update(AIM)
        else:
            player.update(IDLE)

    if shoot:
        player.shoot(bullet_group)
        # players direction will be -1 or +1 depending on which way he is looking
        # print("PLAYERS ")
        # bullet = Bullet(player.rect.centerx + (player.rect.width * .6 * player.direction),
        #                 player.rect.centery, player.direction)
        # bullet_group.add(bullet)

    if granade_throw:
        player.throw_granade(granade_group)

    for bullet in bullet_group.sprites():
        bullet.add_hit_strikes(player, enemy1, bullet_group)

    for item in item_box_group.sprites():
        item.add_player(player, item_box_group)

    for granade in granade_group.sprites():
        granade.add_hit_strike(player, enemy1, granade_group)
    bullet_group.update()
    granade_group.update()

    # if pygame.sprite.spritecollide(player, bullet_group, False):
    #     print("colliding")
    player.update_animation()  # this cannot be inside an event loop.
    enemy.move()
    enemy1.move()
    enemy1.update()

    player.move(move_left, move_right, jump, PLAYER_SPEED, enemy1.rect)
    # Draw all the group entities that are created
    level.refresh_screen(screen, state)
    #screen.fill((0, 0, 0))
    level.create_background(1, scroll)
    pygame.draw.line(screen, (255, 255, 0), (10, 350), (900, 350), 5)
    # level_data = Level()
    # print("scroll:", scroll)
    # level_data.createLevel("one", scroll)

    player.draw(screen)
    item_box_group.update()
    # enemy.draw(screen)
    bullet_group.draw(screen)
    granade_group.draw(screen)
    item_box_group.draw(screen)


    enemy1.draw(screen)

    #player.detect_collission(enemy1.rect)

    # player.move(move_left, move_right, 5)

    # health = int(enemy1.health * 2)
    #
    # pygame.draw.rect(screen, "red", [150, 10, 200, 20])
    # pygame.draw.rect(screen, "green", [150, 10, health, 20])

    generate_bar(screen, './assets/objects/heart.png', 20, 10, enemy1.health, enemy1.max_heath, 'BAR')
    generate_bar(screen, './assets/objects/missile.gif', 330, 10, player.granade_count,
                player.max_granade_count, 'xTEXT', str(player.granade_count))
    generate_bar(screen, './assets/objects/rifle.png', 180, 10, player.ammo, player.max_ammo, .5)
    generate_coins(screen, './assets/objects/coin.png', 500, 10, 5, 1)
    # ft = pygame.font.SysFont('Comic Sans MS', 30)
    # font_surface = ft.render(f"Health: {player.health}", False, (200, 200, 200))
    # screen.blit(font_surface, (10, 10))

    # pygame.draw.rect(screen, pygame.Color(100,100,100, 100), pygame.rect.Rect(100, 100, 100, 100))
    pygame.display.flip()

pygame.quit()