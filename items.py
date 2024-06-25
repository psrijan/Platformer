import pygame.sprite
from enum import Enum


class ItemBoxType(Enum):
    GUN = "rifle"
    BOMB = "missile"
    COIN = "coin"
    HEART = "heart"


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.item_type = item_type
        self.img_dict = {}
        self.scale = 1
        self.image = pygame.image.load(f"./assets/itembox/{self.item_type.value}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.original_size = (self.image.get_width(), self.image.get_height())

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.scale_dir = -1
        self.MIN_SCALE_VALUE = .80
        self.MAX_SCALE_VALUE = 1
        self.player = None
        self.item_group = None

    def add_player(self, player, item_group):
        print('adding player in item box')
        self.player = player
        self.item_group = item_group

    def update(self):
        print("player is none in update :" + str(self.player.rect is None))
        if pygame.sprite.collide_rect(self.player, self):
            self.player.add_inventory(self.item_type)
            self.kill()


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'./assets/level_data/mapping/{img}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Decoration(pygame.sprite.Sprite):

    def __init__(self, img,x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load(f'./assets/level_data/mapping/{img}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Water(pygame.sprite.Sprite):

    def __init__(self, img, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load(f'./assets/level_data/mapping/{img}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
