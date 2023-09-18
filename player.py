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
        imgTags = [AIM, DEATH, IDLE, RUN, SHOOT]
        self.animationFileMap = {}
        self.update_time = pygame.time.get_ticks()
        for curTag in imgTags:
            fileList = os.listdir(f'assets/player/{curTag}')
            self.animationFileMap[curTag] = fileList

        self.state = IDLE
        self.direction = IDLE
        self.jump = False
        self.scale = scale
        self.index = 0
        self.x = x
        self.y = y
        self.idle()

    def idle(self):
        # initialize state to idle if it's not the case and index img to 0
        if self.state not in IDLE:
            self.state = IDLE
            self.index = 0
        print('State: {} Index: {} Total Size: {} '.format(self.state, self.index, len(self.animationFileMap[self.state])) )
        self.img = pygame.image.load(
            'assets/player/{}/{}'.format(self.state, self.animationFileMap[self.state][self.index]))
        self.img = pygame.transform.scale(self.img, (
        int(self.img.get_width() * self.scale), int(self.img.get_height() * self.scale)))
        self.index = (self.index + 1) % len(self.animationFileMap[self.state])
        print('img index: {}'.format(self.index))

    def draw(self, screen):
        self.rect = self.img.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)

    def move(self, move_left, move_right, isJump, speed):
        dx = 0
        dy = 0
        if move_left:
            dx = -speed
            if self.direction not in 'LEFT':
                self.state = RUN
                self.direction = 'LEFT'
                self.index = 0
            self.img = pygame.image.load('assets/player/{}/{}'.format(self.state, self.animationFileMap[self.state][self.index]))
            self.img = pygame.transform.scale(pygame.transform.flip(self.img, True, False),
                                              (int(self.img.get_width() * self.scale),
                                               int(self.img.get_height() * self.scale)))
            self.index = (self.index + 1) % len(self.animationFileMap[RUN])

        elif move_right:
            dx = speed
            if self.direction not in 'RIGHT':
                self.state = RUN
                self.direction = 'RIGHT'
                self.index = 0
            self.img = pygame.image.load('assets/player/{}/{}'.format(self.state, self.animationFileMap[self.state][self.index]))
            self.img = pygame.transform.scale(self.img, (int(self.img.get_width() * self.scale),
                                               int(self.img.get_height() * self.scale)))
            # self.img = pygame.transform.flip(self.img, 1, 0)
            self.index = (self.index + 1) % len(self.animationFileMap[RUN])

        elif not move_left and not move_right:
            if self.direction not in 'IDLE':
                self.direction = IDLE
                self.index = 0
                self.state = IDLE # start and direction same here

            self.idle()

        if self.jump != isJump:
            self.jump = isJump

        print('change in x: ')
        self.x += dx
        self.y += dy


    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.index += 1
            self.update_time = pygame.time.get_ticks()


    def update_player_action(self, action):
        if self.state != action:
            self.state = action
            self.index = 0
            self.update_time = pygame.time.get_ticks()

