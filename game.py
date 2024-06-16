import pygame
from player import Soldier, Bullet, Granade
import time
from enemy import Enemy
from imageutil import clip2
from items import ItemBox, ItemBoxType

SCREEN_WIDTH = 768
SCREEN_HEIGHT = 432

class Level(object):
    def __init__(self, level=1):
        self.cur_level = level
        self.pygame = pygame

        self.img_list = []

        for i in range(1, 6):
            img = pygame.image.load(f"./assets/levels/one/plx-{i}.png").convert_alpha()
            self.img_list.append(img)
    def createLevel(self, level, scroll):
        #screen.blit((0,0,0))
        speed = 1
        for x in range(0, 4):
            for i in range (0, len(self.img_list)):
                img = self.img_list[i]
                img = self.img_list[i]
                screen.blit(img, (x * img.get_width() + scroll * speed, 0))
                speed += .2


def generateCoins(imgLoc, startX, startY, count, scale=1):
    img = pygame.image.load(imgLoc).convert_alpha()
    img = clip2(img, 0, 0, 20, 20)
    img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
    offset = 22 # keeping a default offset of 20px
    for i in range(0, count):
        rect = img.get_rect()
        rect.centerx = startX + offset * i
        rect.centery = startY
        screen.blit(img, rect)

def generateBar(imgLoc, startX, startY, amountLeft, totalAmount, bar_type, text='', scale=1):
    pass
    # ft = pygame.font.SysFont('Comic Sans MS', 30)
    # font_surface = ft.render("hello world", False, (200, 200, 200))
    # screen.blit(font_surface, (10, 10))
    img = pygame.image.load(imgLoc).convert_alpha()
    img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
    img.get_rect()

    print("heart: ", img.get_width(), " - ", img.get_height())
    img_rect = img.get_rect()
    img_rect.center = (startX, startY)
    screen.blit(img, img_rect)
    width = 100
    height = 10
    actual_width = int((amountLeft * width) / totalAmount)

    if bar_type == 'BAR':
        pygame.draw.rect(screen, "white",  [startX + 14, startY - 2, width + 4, 10 + 4])
        pygame.draw.rect(screen, "red", [startX + 16, startY, width, height])
        pygame.draw.rect(screen, "green", [startX + 16, startY, actual_width, height])
    elif bar_type == 'xTEXT':
        ft = pygame.font.SysFont('Comic Sans MS', 11)
        font_surface = ft.render('X {}'.format(text), False, (200, 200, 200))
        screen.blit(font_surface, (startX + 30, startY))


PLAYER_SPEED = 15

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
granade_throw = False

IDLE = 'idle'
RUN = 'run'
SHOOT = 'shoot'
AIM = 'aim'

FPS = 60

pygame.draw.rect(screen, "green",[75, 10, 50, 20])

# bullet group to hold the bullets created by the user
bullet_group = pygame.sprite.Group()
granade_group = pygame.sprite.Group()
scroll = 1
hasGameStarted = False

while GAME_LOOP_RUNNING:

    clock.tick(FPS)
    key = pygame.key.get_pressed()
    if key[pygame.K_a] and scroll > 0:
        scroll -= 5
    if key[pygame.K_d] and scroll < 3000:
        scroll += 5

    scroll = 0 # remove for parallex after fixing the player issue

    print("SCROLL: ", scroll)

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
        player.throwGranade(granade_group)

    for bullet in bullet_group.sprites():
        bullet.add_hit_strikes(player, enemy1, bullet_group)

    for granade in granade_group.sprites():
        granade.add_hit_strike(player, enemy1, granade_group)
    bullet_group.update()
    granade_group.update()

    player.move(move_left, move_right, jump, PLAYER_SPEED)
    enemy.move()
    enemy1.move()
    enemy1.update()

    screen.fill((0, 0, 0))
    # level = Level()
    # print("scroll:", scroll)
    # level.createLevel("one", scroll)

    player.draw(screen)
    # enemy.draw(screen)
    enemy1.draw(screen)
    bullet_group.draw(screen)
    granade_group.draw(screen)

    player.detect_collission(enemy1.rect)

    # player.move(move_left, move_right, 5)

    # health = int(enemy1.health * 2)
    #
    # pygame.draw.rect(screen, "red", [150, 10, 200, 20])
    # pygame.draw.rect(screen, "green", [150, 10, health, 20])

    generateBar('./assets/objects/heart.png', 20, 10, enemy1.health, enemy1.max_heath, 'BAR')
    generateBar('./assets/objects/missile.gif', 330, 10, player.granade_count,
                player.max_granade_count, 'xTEXT', str(player.granade_count))
    generateBar('./assets/objects/rifle.png', 180, 10, player.ammo, player.max_ammo, .5)
    generateCoins('./assets/objects/coin.png', 500, 10, 5, 1)
    # ft = pygame.font.SysFont('Comic Sans MS', 30)
    # font_surface = ft.render(f"Health: {player.health}", False, (200, 200, 200))
    # screen.blit(font_surface, (10, 10))

    # pygame.draw.rect(screen, pygame.Color(100,100,100, 100), pygame.rect.Rect(100, 100, 100, 100))
    pygame.display.flip()
    pygame.time.delay(150)  # @todo check if this is a way to delay frame rate in python.

pygame.quit()