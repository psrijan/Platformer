import pygame
import os

from enum import Enum

AIM = 'aim'
DEATH = 'death'
IDLE = 'idle'
RUN = 'run'
SHOOT = 'shoot'

PLAYER_SPEED = 5

class Soldier(pygame.sprite.Sprite):

    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self) # i don't quite understand this
        self.alive = True
        self.rect = None
        self.img = None
        self.flip = False
        imgTags = [AIM, DEATH, IDLE, RUN, SHOOT]
        self.animationFileMap = {}
        self.update_time = pygame.time.get_ticks()
        for curTag in imgTags:
            fileList = os.listdir(f'assets/player/{curTag}')
            self.animationFileMap[curTag] = fileList

        self.action = IDLE
        self.direction = IDLE
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
        print('State: {} Index: {} Total Size: {} '.format(self.action, self.index, len(self.animationFileMap[self.action])))
        self.img = pygame.image.load(
            'assets/player/{}/{}'.format(self.action, self.animationFileMap[self.action][self.index]))
        self.img = pygame.transform.scale(self.img, (
        int(self.img.get_width() * self.scale), int(self.img.get_height() * self.scale)))
        self.index = (self.index + 1) % len(self.animationFileMap[self.action])
        print('img index: {}'.format(self.index))

    def draw(self, screen):
        self.img = pygame.image.load(
            'assets/player/{}/{}'.format(self.action, self.animationFileMap[self.action][self.index]))
        self.img = pygame.transform.scale(pygame.transform.flip(self.img, self.flip, False),
                                          (int(self.img.get_width() * self.scale),
                                           int(self.img.get_height() * self.scale)))
        self.index = (self.index + 1) % len(self.animationFileMap[self.action])
        self.rect = self.img.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)

    def move(self, move_left, move_right, isJump, speed):
        dx = 0
        dy = 0
        if move_left:
            dx = -speed
            self.flip = True
            self.direction = -1
        elif move_right:
            dx = speed
            self.flip = False
            self.direction = 1

        self.x += dx
        self.y += dy


    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.index += 1
            self.update_time = pygame.time.get_ticks()


    def update_player_action(self, cur_action):
        if self.action != cur_action:
            self.action = cur_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()

