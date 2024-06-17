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
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
        self.original_size = (self.image.get_width(), self.image.get_height())

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.scale_dir = -1
        self.MIN_SCALE_VALUE = .80
        self.MAX_SCALE_VALUE = 1
        self.player = None
        self.item_group = None

    def add_player(self, player, item_group):
        self.player = player
        self.item_group = item_group

    def update(self):

        # if self.scale > self.MIN_SCALE_VALUE and self.scale_dir == - 1 or self.scale < self.MAX_SCALE_VALUE and self.scale_dir == 1:
        #     self.scale = self.scale + .02 * self.scale_dir
        # elif self.scale < self.MIN_SCALE_VALUE:
        #     self.scale = self.MIN_SCALE_VALUE + .02
        #     self.scale_dir = self.scale_dir * -1
        # else:
        #     self.scale = self.MAX_SCALE_VALUE - .02
        #     self.scale_dir = self.scale_dir * -1
        #     print(f"Changing Scale Direction: scale : {self.scale}  direction -  {self.scale_dir}")
        # self.image = pygame.transform.scale(self.image, (self.original_size[0] * self.scale, self.original_size[1] * self.scale))

        # print("updating item box")
        pass

