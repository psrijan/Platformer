import pygame
class GameState:
    def __init__(self):
        # bullet group to hold the bullets created by the user
        self.bullet_group = pygame.sprite.Group()
        self.granade_group = pygame.sprite.Group()
        self.item_box_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.decoration_group = pygame.sprite.Group()
