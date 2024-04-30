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
    dy = 0

    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)  # i don't quite understand this
        self.isJumpActivated = False
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
        self.jump = False
        self.scale = scale
        self.index = 0
        self.x = x
        self.y = y
        self.idle()

    def idle(self):# encoding: utf-8
# module pygame.transform
# from /home/srijan/Documents/code/Platformer/env/lib/python3.10/site-packages/pygame/transform.cpython-310-x86_64-linux-gnu.so
# by generator 1.147
""" pygame module to transform surfaces """
# no imports

# functions

def average_color(surface, rect=None, consider_alpha=False): # real signature unknown; restored from __doc__
    """
    average_color(surface, rect=None, consider_alpha=False) -> Color
    finds the average color of a surface
    """
    pass

def average_surfaces(surfaces, dest_surface=None, palette_colors=1): # real signature unknown; restored from __doc__
    """
    average_surfaces(surfaces, dest_surface=None, palette_colors=1) -> Surface
    find the average surface from many surfaces.
    """
    pass

def chop(surface, rect): # real signature unknown; restored from __doc__
    """
    chop(surface, rect) -> Surface
    gets a copy of an image with an interior area removed
    """
    pass

def flip(surface, flip_x, flip_y): # real signature unknown; restored from __doc__
    """
    flip(surface, flip_x, flip_y) -> Surface
    flip vertically and horizontally
    """
    pass

def get_smoothscale_backend(): # real signature unknown; restored from __doc__
    """
    get_smoothscale_backend() -> string
    return smoothscale filter version in use: 'GENERIC', 'MMX', or 'SSE'
    """
    return ""

def grayscale(surface, dest_surface=None): # real signature unknown; restored from __doc__
    """
    grayscale(surface, dest_surface=None) -> Surface
    grayscale a surface
    """
    pass

def laplacian(*args, **kwargs): # real signature unknown
    """
    threshold(dest_surface, surface, search_color, threshold=(0,0,0,0), set_color=(0,0,0,0), set_behavior=1, search_surf=None, inverse_set=False) -> num_threshold_pixels
    finds which, and how many pixels in a surface are within a threshold of a 'search_color' or a 'search_surf'.
    """
    pass

def rotate(surface, angle): # real signature unknown; restored from __doc__
    """
    rotate(surface, angle) -> Surface
    rotate an image
    """
    pass

def rotozoom(surface, angle, scale): # real signature unknown; restored from __doc__
    """
    rotozoom(surface, angle, scale) -> Surface
    filtered scale and rotation
    """
    pass

def scale(surface, size, dest_surface=None): # real signature unknown; restored from __doc__
    """
    scale(surface, size, dest_surface=None) -> Surface
    resize to new resolution
    """
    pass

def scale2x(surface, dest_surface=None): # real signature unknown; restored from __doc__
    """
    scale2x(surface, dest_surface=None) -> Surface
    specialized image doubler
    """
    pass

def scale_by(surface, factor, dest_surface=None): # real signature unknown; restored from __doc__
    """
    scale_by(surface, factor, dest_surface=None) -> Surface
    resize to new resolution, using scalar(s)
    """
    pass

def set_smoothscale_backend(backend): # real signature unknown; restored from __doc__
    """
    set_smoothscale_backend(backend) -> None
    set smoothscale filter version to one of: 'GENERIC', 'MMX', or 'SSE'
    """
    pass

def smoothscale(surface, size, dest_surface=None): # real signature unknown; restored from __doc__
    """
    smoothscale(surface, size, dest_surface=None) -> Surface
    scale a surface to an arbitrary size smoothly
    """
    pass

def smoothscale_by(surface, factor, dest_surface=None): # real signature unknown; restored from __doc__
    """
    smoothscale_by(surface, factor, dest_surface=None) -> Surface
    resize to new resolution, using scalar(s)
    """
    pass

def threshold(dest_surface, surface, search_color, threshold=(0,0,0,0), set_color=(0,0,0,0), set_behavior=1, search_surf=None, inverse_set=False): # real signature unknown; restored from __doc__
    """
    threshold(dest_surface, surface, search_color, threshold=(0,0,0,0), set_color=(0,0,0,0), set_behavior=1, search_surf=None, inverse_set=False) -> num_threshold_pixels
    finds which, and how many pixels in a surface are within a threshold of a 'search_color' or a 'search_surf'.
    """
    pass

# no classes
# variables with complex values

__loader__ = None # (!) real value is '<_frozen_importlib_external.ExtensionFileLoader object at 0x7d24fff2a740>'

__spec__ = None # (!) real value is "ModuleSpec(name='pygame.transform', loader=<_frozen_importlib_external.ExtensionFileLoader object at 0x7d24fff2a740>, origin='/home/srijan/Documents/code/Platformer/env/lib/python3.10/site-packages/pygame/transform.cpython-310-x86_64-linux-gnu.so')"


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
        print('img index: {}'.format(self.index))

    def draw(self, screen):
        self.img = pygame.image.load(
            'assets/player/{}/{}'.format(self.action, self.animationFileMap[self.action][self.index]))
        print("Action : {} Index: {} ".format(self.action, self.index))
        self.img = pygame.transform.scale(pygame.transform.flip(self.img, self.flip, False),
                                          (int(self.img.get_width() * self.scale),
                                           int(self.img.get_height() * self.scale)))
        self.index = (self.index + 1) % len(self.animationFileMap[self.action])
        self.rect = self.img.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)

    ySpeed = 15

    def move(self, move_left, move_right, isJump, speed):
        dx = 0

        print('move activated')

        if move_left:
            dx = -speed
            self.flip = True
        elif move_right:
            dx = speed
            self.flip = False

        if isJump:
            self.isJumpActivated = True

        if self.isJumpActivated:
            self.ySpeed = self.ySpeed - .5
            dy = self.ySpeed
        else:
            dy = 0

        self.x += dx
        self.y -= dy

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
