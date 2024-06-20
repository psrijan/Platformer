import pygame
import os
from pygame import Rect
from pygame.sprite import Group
from enum import Enum
from sounds import SoundModule
from items import ItemBox, ItemBoxType

AIM = 'aim'
DEATH = 'death'
IDLE = 'idle'
RUN = 'run'
SHOOT = 'shoot'

PLAYER_SPEED = 5
MAX_GRANADE = 5
MAX_AMMO = 100
MAX_COIN = 250
MAX_HEALTH = 100

RIGHT = 1
LEFT = -1
TERMINAL_VELOCITY = 10


class Soldier(pygame.sprite.Sprite):
    dy = 0

    def __init__(self, x, y, scale, speed=10, ammo=10, health=90, granade=5):
        pygame.sprite.Sprite.__init__(self)  # i don't quite understand this
        self.shoot_time = 0  # Putting a 50 millisecond shoot cool downt time
        self.grande_throw_time = 0
        self.SHOOT_COOLDOWN_TIME = 350
        self.GRANDE_COOLDOWN_TIME = 700
        self.isJumpActivated = False
        self.alive = True
        self.direction = RIGHT  # initially player is looking at the right side
        self.rect = None
        self.img = None
        self.flip = False
        self.aim_major_loop = False
        imgTags = [AIM, DEATH, IDLE, RUN, SHOOT]
        self.animationFileMap = {}
        self.update_time = pygame.time.get_ticks()
        self.move_time = pygame.time.get_ticks()
        self.gravity = .75
        self.coin = 0

        self.ammo = ammo
        self.max_ammo = ammo

        self.max_granade_count = granade
        self.granade_count = granade

        self.health = health
        self.max_health = health
        self.sound_module = SoundModule()

        for curTag in imgTags:
            fileList = os.listdir(f'assets/player/{curTag}')
            loaded_files = []
            for file_name in fileList:
                # print(f'./assets/player/{curTag}/{file_name}')
                load_img = pygame.image.load(f'assets/player/{curTag}/{file_name}').convert_alpha()
                loaded_files.append(load_img)
                self.animationFileMap[curTag] = loaded_files

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

    def add_inventory(self, item_type):
        if item_type == ItemBoxType.GUN:
            self.ammo += 25
            self.ammo = min(100, self.ammo)
        elif item_type == ItemBoxType.BOMB:
            self.granade_count = min(MAX_GRANADE, self.granade_count + 25)
        elif item_type == ItemBoxType.HEART:
            self.health = max(self.health + 25, MAX_HEALTH)
        elif item_type == ItemBoxType.COIN:
            self.coin += 1

    def idle(self):
        # initialize state to idle if it's not the case and index img to 0
        if self.action not in IDLE:
            self.action = IDLE
            self.index = 0
        print('State: {} Index: {} Total Size: {} '.format(self.action, self.index,
                                                           len(self.animationFileMap[self.action])))
        self.img = self.animationFileMap[self.action][self.index]
        self.img = pygame.transform.scale(self.img, (
            int(self.img.get_width() * self.scale), int(self.img.get_height() * self.scale)))
        # self.index = (self.index + 1) % len(self.animationFileMap[self.action])

    def draw(self, screen):

        # AIM needs to iterate through two different set of image set for animation
        if self.action == 'aim':
            if self.aim_major_loop and self.index == 0:
                self.index += 3
                self.index = self.index % len(self.animationFileMap[self.action])
            elif self.index > 3 and not self.aim_major_loop:
                self.aim_major_loop = True
        print("index in draw for player:" , str(self.index))
        self.img = self.animationFileMap[self.action][self.index]
        self.img = pygame.transform.scale(pygame.transform.flip(self.img, self.flip, False),
                                          (int(self.img.get_width() * self.scale),
                                           int(self.img.get_height() * self.scale)))
        # self.index = (self.index + 1) % len(self.animationFileMap[self.action])
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
            self.sound_module.shoot()
        else:
            print("player ammo empty or shoot time not exceeded ")

    def throwGranade(self, granade_group: Group):
        cur_ticks = pygame.time.get_ticks()
        if cur_ticks - self.grande_throw_time > self.GRANDE_COOLDOWN_TIME and self.granade_count > 0:
            self.sound_module.launch_granade()
            print('throwing grande')
            granade = Granade(self.rect.centerx + (self.rect.width * .6 * self.direction),
                              self.rect.centery, self.direction)
            granade_group.add(granade)
            self.granade_count -= 1
            self.grande_throw_time = pygame.time.get_ticks()
        else:
            print("player granade box empty or throw time not exceeded")

    def update(self, action):
        self.update_player_action(action)

    def move(self, move_left, move_right, isJump, speed, enemy):
        dx = 0

        if move_left:
            self.direction = LEFT
            dx = -speed
            self.flip = True
        elif move_right:
            self.direction = RIGHT
            dx = speed
            self.flip = False

        INITIAL_Y_SPEED = -10
        if isJump:
            self.ySpeed = INITIAL_Y_SPEED
            self.isJumpActivated = True
            self.sound_module.jump()

        if self.isJumpActivated:
            self.ySpeed = self.ySpeed + self.gravity
            dy = self.ySpeed
            if self.ySpeed > TERMINAL_VELOCITY:
                self.ySpeed = TERMINAL_VELOCITY  # terminal velocity (10)
        else:
            dy = 0

        check_x_collission = self.detect_x_collission(self.x, dx, self.direction, enemy)
        check_y_collission = self.detect_y_collission(self.y, dy, 0)

        if check_y_collission[0]:
            self.ySpeed = 0
            self.isJumpActivated = False

        self.x = check_x_collission[1]
        self.y = check_y_collission[1]

    def detect_x_collission(self, cur_x, dx, direction, rect: Rect):
        next_x_pos = cur_x + dx
        # checking if next_x_pos is inside the coordinate, return co-ordinate between LEFT and RIGHT VARRIES, check logic should be the same

        is_collided = next_x_pos >= rect.centerx - rect.width // 2 and next_x_pos <= rect.centerx + rect.width // 2
        if not is_collided:
            return (False, cur_x + dx)

        if direction == LEFT:
            print('collided: left')
            return (True, rect.centerx + rect.width // 2 + 2)
        # checking if next_x position falls inside the coordinates of th rectangle
        else:
            print('collided: left')
            return (True, rect.centerx - rect.width // 2 - 2)

    def detect_y_collission(self, cur_y, dy, direction):
        TEMP_EARTH_LOCATION = 350
        next_y_pos = cur_y + dy

        is_collided = next_y_pos + self.img.get_rect().height // 2 > TEMP_EARTH_LOCATION  # current base

        if is_collided:
            return (True, 350 - self.img.get_rect().height // 2)
        else:
            return (False, next_y_pos)

    # rect collide list would result in identifying the list of elements
    # pygame rect would collide with so any thing that you think it would collide to
    # we can add into the list and test out and the result would be the index of the object
    def detect_collission(self, rect: Rect):
        is_collide = rect.colliderect(self.rect)
        if is_collide:
            print(' The player is colliding at this time ')
            if self.direction == LEFT:
                self.x = rect.x + rect.width
                self.y = 300

    def update_animation(self):
        print('update animation in player')
        ANIMATION_COOLDOWN = 100
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.index = (self.index + 1) % len(self.animationFileMap[self.action])
            self.update_time = pygame.time.get_ticks()
            print(f"updating_animation: {self.index}")

    def update_player_action(self, cur_action):
        print("update player action being called")
        if self.action != cur_action:
            self.action = cur_action
            self.index = 0
            # aim has two set of animation, a start animation and second
            self.aim_major_loop = False
            self.update_time = pygame.time.get_ticks() # seems like a default value


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_group = None
        self.player: Soldier = None
        self.enemy = None
        self.image = pygame.image.load("./assets/golum/PROJECTILE.png").convert_alpha()

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
        print("ITEMS: ", items)
        self.state_image["FLYING"] = [pygame.image.load("./assets/objects/missile.gif").convert()]
        exploding_img_list = []
        for imageItem in sorted(items):
            img = pygame.image.load(f"./assets/PixelSimulations/Explosion4/{imageItem}").convert_alpha()
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
        self.sound_module = SoundModule()
        self.is_playing_sound = False

    # This is meant to add all element to collide with
    def add_hit_strike(self, player, enemy, granade_group):
        print("Hit strike granade")
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
                if not self.is_playing_sound:
                    self.is_playing_sound = True
                    self.sound_module.explosion()
                    self.check_collission([self.enemy])
        else:
            self.index = 0  # flying just use the first index

    def check_collission(self, enemy_list: pygame.sprite.Sprite):
        for entity in enemy_list:
            if pygame.sprite.spritecollide(entity, self.granade_group, False):
                print("granade explosion colliding with someone")
                entity.health -= 50