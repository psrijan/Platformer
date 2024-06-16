import pygame.sprite
from enum import Enum

class ItemBoxType(Enum):
    GUN = "rifle"
    BOMB = "missile"
    COIN = "coin"
    HEART = "heart"

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.img_dict = {}
        img = pygame.image.load(f"./assets/objects/{self.item_type}.png")



    def draw(self, screen):
        pass


