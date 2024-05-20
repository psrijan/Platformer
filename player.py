import pygame
import os
from pygame import Rect
from pygame.sprite import Group
from enum import Enum

AIM = 'aim'
DEATH = 'death'
IDLE = 'idle'
RUN = 'run'
SHOOT = 'shoot'

PLAYER_SPEED = 5


class Soldier(pygame.sprite.Sprite):
    dy = 0

    def __init__(self, x, y, scale, speed=10, ammo=10, health=90, granade=5):
        pygame.sprite.Sprite.__init__(self)  # i don't quite understand this
        self.shoot_time = 0  # Putting a 50 millisecond shoot cool downt time
        self.grande_throw_time = 0
        self.SHOOT_COOLDOWN_TIME = 300
        self.GRANDE_COOLDOWN_TIME = 700
        self.isJumpActivated = False
        self.alive = True
        self.direction = 1  # initially player is looking at the right side
        self.rect = None
        self.img = None
        self.flip = False
        self.aim_major_loop = False
        imgTags = [AIM, DEATH, IDLE, RUN, SHOOT]
        self.animationFileMap = {}
        self.update_time = pygame.time.get_ticks()
        self.gravity = .75

        self.ammo = ammo
        self.max_ammo = ammo

        self.max_granade_count = granade
        self.granade_count = granade

        self.health = health
        self.max_health = health

        for curTag in imgTags:
            fileList = os.listdir(f'assets/player/{curTag}')
            self.animationFileMap[curTag] = sorted(fileList)

            # if curTag == 'aim':
            #     print(sorted(fileList))
            #     print(len(fileList))
            #     exit(0)

        self.action = IDLE
        self.jump = False
        self.scale = scale
        self.index = 0
        self.x = x
        self.y = y
        self.idle()

    def idle(self):
        # initialize state to idle if it's not the case and index img to 0
        if self.action not in IDLE:
            self.action = IDLE
            self.index = 0
        print('State: {} Index: {} Total Size: {} '.format(self.action, self.index,
                                                           len(self.animationFileMap[self.action])))
        self.img = pygame.image.load(
            'assets/player/{}/{}'.format(self.action, self.animationFileMap[self.action][self.index]))
        self.img = pygame.transform.scale(self.img, (
            int(self.img.get_width() * self.scale), int(self.img.get_height() * self.scale)))
        self.index = (self.index + 1) % len(self.animationFileMap[self.action])

    def draw(self, screen):

        # AIM needs to iterate through two different set of image set for animation
        if self.action == 'aim':
            if self.aim_major_loop and self.index == 0:
                self.index += 3
                self.index = self.index % len(self.animationFileMap[self.action])
            elif self.index > 3 and not self.aim_major_loop:
                self.aim_major_loop = True

        print('ACTION: {} -- MAJOR LOOP: {} -- INDEX: {} size: {}'.format(self.action, str(self.aim_major_loop),
                                                                          self.index,
                                                                          len(self.animationFileMap[self.action])))

        self.img = pygame.image.load(
            'assets/player/{}/{}'.format(self.action, self.animationFileMap[self.action][self.index]))
        self.img = pygame.transform.scale(pygame.transform.flip(self.img, self.flip, False),
                                          (int(self.img.get_width() * self.scale),
                                           int(self.img.get_height() * self.scale)))
        self.index = (self.index + 1) % len(self.animationFileMap[self.action])
        self.rect = self.img.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)

    ySpeed = 11

    def shoot(self, bullet_group: Group):
        cur_ticks = pygame.time.get_ticks()

        if cur_ticks - self.shoot_time > self.SHOOT_COOLDOWN_TIME and self.ammo > 0:
            print("player is shooting ")
            bullet = Bullet(self.rect.centerx + (self.rect.width * .6 * self.direction),
                            self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
            self.shoot_time = pygame.time.get_ticks()
        else:
            print("player ammo empty or shoot time not exceeded ")

    def throwGranade(self, granade_group: Group):
        cur_ticks = pygame.time.get_ticks()
        if cur_ticks - self.grande_throw_time > self.GRANDE_COOLDOWN_TIME and self.granade_count > 0:
            print('throwing grande')
            granade = Granade(self.rect.centerx + (self.rect.width * .6 * self.direction),
                              self.rect.centery, self.direction)
            granade_group.add(granade)
            self.granade_count -= 1
            self.grande_throw_time = pygame.time.get_ticks()
        else:
            print("player granade box empty or throw time not exceeded")

    def update(self):
        self.update_animation()

    def move(self, move_left, move_right, isJump, speed):
        dx = 0

        if move_left:
            self.direction = -1
            dx = -speed
            self.flip = True
        elif move_right:
            self.direction = 1
            dx = speed
            self.flip = False

        if isJump:
            self.ySpeed = 11
            self.isJumpActivated = True

        if self.isJumpActivated:
            self.ySpeed = self.ySpeed - self.gravity
            dy = self.ySpeed
            if self.ySpeed < - 10:
                self.ySpeed = -10  # terminal velocity
        else:
            dy = 0

        self.x += dx
        self.y -= dy

    # rect collidelist would result in identifying the list of elements
    # pygame rect would collide with so any thing that you think it would collide to
    # we can add into the list and test out and the result would be the index of the object
    def detect_collission(self, rect: Rect):
        is_collide = rect.colliderect(self.rect)
        if is_collide:
            print(' The player is colliding at this time ')
            if self.direction == -1:
                self.x = rect.x + rect.width
                self.y = 300

    def update_animation(self):
        ANIMATION_COOLDOWN = 50
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.index += 1
            self.update_time = pygame.time.get_ticks()

    def update_player_action(self, cur_action):
        if self.action != cur_action:
            self.action = cur_action
            self.index = 0
            # aim has two set of animation, a start animation and second
            self.aim_major_loop = False
            self.update_time = pygame.time.get_ticks()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_group = None
        self.player : Soldier = None
        self.enemy = None
        self.image = pygame.image.load("./assets/golum/PROJECTILE.png")

        self.direction = direction
        flipX = False

        if self.direction == 1:
            flipX = True

        self.image = pygame.transform.scale(pygame.transform.flip(self.image, flipX, False),
                                            (self.image.get_width() * .5, self.image.get_height() * .75))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 20

    def add_hit_strikes(self, player, enemy, bullet_group):
        print("add hit strike called ")
        self.player = player
        self.enemy = enemy
        self.bullet_group = bullet_group


    def update(self):
        self.rect.x += (self.speed * self.direction)

        # check if bullet goes out of screen
        if self.rect.right < 0 or self.rect.left > 1280:
            self.kill()

        # need to change this logic,
        # need to find a better way of gettings these objects
        if pygame.sprite.spritecollide(self.player, self.bullet_group, False):
            if self.player.alive:
                self.player.health -= 5
                self.kill()

        if pygame.sprite.spritecollide(self.enemy, self.bullet_group, False):
            if self.enemy.alive:
                self.kill()
                self.enemy.health -= 25


class Granade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.state = ["EXPLODING", "FLYING"]
        self.cur_state = "FLYING"
        self.image = pygame.image.load("./assets/objects/missile.gif")
        self.state_image = {}
        items = os.listdir("./assets/PixelSimulations/Explosion4/")
        print("ITEMS: " , items)
        self.state_image["FLYING"] = [pygame.image.load("./assets/objects/missile.gif").convert()]
        exploding_img_list = []
        for imageItem in sorted(items):
            img = pygame.image.load(f"./assets/PixelSimulations/Explosion4/{imageItem}").convert()
            exploding_img_list.append(img)
        self.state_image["EXPLODING"] = exploding_img_list
        if direction == 1:
            self.flipX = False
        else:
            self.flipX = True
        self.image = pygame.transform.flip(self.image, self.flipX, False)
        self.direction = direction
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.start_time = pygame.time.get_ticks()
        self.gravity = 2
        self.speed = 10
        self.speedY = 2
        self.gravity = .5
        self.bobLeft = True
        self.index = 0

    def add_hit_strike(self, player, enemy, granade_group):
        self.player = player
        self.enemy = enemy
        self.granade_group = granade_group

    def update(self):
        print("Update class is being called")
        self.image = self.state_image[self.cur_state][self.index]
        if self.cur_state == "FLYING":
            self.rect.x += (self.speed * self.direction)
            self.rect.y -= self.speedY
        if self.speedY < 15:
            self.speedY -= self.gravity
        if self.bobLeft:
            self.image = pygame.transform.rotate(self.image, -.2)
        else:
            self.image = pygame.transform.rotate(self.image, +.2)
        self.bobLeft = not self.bobLeft

        if pygame.time.get_ticks() - self.start_time >= 3000 and self.cur_state is not "EXPLODING":
            print("bomb time elapsed")
            self.cur_state = "EXPLODING"
            self.index = 0

        if self.cur_state == "EXPLODING":
            if not self.index == len(self.state_image[self.cur_state]) - 1:
                self.index = (self.index + 1) % len(self.state_image[self.cur_state])
        else:
            self.index = 0 # flying just use the first index


