import pygame.sprite
import os


class Golum(pygame.sprite.Sprite):

    def __init__(self, x, y, scale, enemyType):
        pygame.sprite.Sprite.__init__(self)  # i don't quite understand this
        self.rect = None
        self.img = None
        self.x = x
        self.y = y
        self.enemyType = enemyType
        self.animationFileMap = {}
        GOLUM_STATES = ['ATTACK', 'DEATH', 'FLYING', 'HURT', 'IDLE', 'PROJECTILE']

        # for state in GOLUM_STATES:
        #     file = os.listdir(f'assets/golum/{state}.png')
        #     self.animationFileMap[state] = fileList

        self.img = pygame.image.load(f'assets/golum/{IDLE}.png')
        self.img = pygame.transform.scale(pygame.transform.flip((self.img, False, False)),
                                          (int(self.img.get_width() * self.scale, int(self.img.get_height() * self.scale))),
                                          )

    def draw(self, screen):
        self.rect = self.img.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)
