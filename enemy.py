import pygame.sprite
from imageutil import clip

static_data = {
    'FLYING': {
        'IMG_COUNT': 4,
        'IMAGE_SIZE': [(81, 71), (81, 71), (81, 71), (81, 71)],
        'IMAGE_COORD': [(0, 0), (81, 0), (162, 0), (244, 0)]
    },
    'HURT': {
        'IMG_COUNT': 4,
        'IMAGE_SIZE': [(81, 71), (81, 71), (81, 71), (81, 71)],
        'IMAGE_COORD': [(0, 0), (81, 0), (162, 0), (244, 0)]
    },
    'IDLE': {
        'IMG_COUNT': 4,
        'IMAGE_SIZE': [(81, 71), (81, 71), (81, 71), (81, 71)],
        'IMAGE_COORD': [(0, 0), (81, 0), (162, 0), (244, 0)]
    },
    'DEATH': {
        'IMG_COUNT': 6,
        'IMAGE_SIZE': [(81, 71), (81, 71), (81, 71), (81, 71), (81, 71), (81, 71)],
        'IMAGE_COORD': [(0, 0), (81, 0), (162, 0), (244, 0), (325, 0), (406, 0)]
    },'ATTACK': {
        'IMG_COUNT': 8,
        'IMAGE_SIZE': [(81, 71), (81, 71), (81, 71), (81, 71), (81, 71), (81, 71),(81, 71),(81, 71)],
        'IMAGE_COORD': [(0, 0), (81, 0), (162, 0), (244, 0), (325, 0), (406, 0), (487, 0), (568, 0)]
    },
}


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, cur_state='IDLE'):
        pygame.sprite.Sprite.__init__(self)
        self.flip = True
        self.img = None
        self.x = x
        self.y = y
        self.index = 0
        self.CENTER = self.x  # moves around across the initial value of center
        self.scale = scale
        self.img_map = {}

        self.cur_state = cur_state
        self.state = ['ATTACK', 'DEATH', 'FLYING', 'HURT', 'IDLE']
        if self.cur_state == 'IDLE':
            self.dx = 0
        else:
            self.dx = 15  # horizontal speed of the golum
        self.dy = 0  # vertical speed of the golum
        self.static_data = static_data

        for cur_state in self.state:
            img_surface = pygame.image.load('./assets/golum/{}.png'.format(cur_state))
            self.img_map[cur_state] = img_surface

    def draw(self, screen):
        state_img_list = self.img_map[self.cur_state]
        max_index = static_data[self.cur_state]['IMG_COUNT']
        img_size = static_data[self.cur_state]['IMAGE_SIZE'][self.index]
        img_coord = static_data[self.cur_state]['IMAGE_COORD'][self.index]
        print(f'ENEMY - cur_index {self.index} max_index {max_index} img_size {img_size} img_coord {img_coord} ')
        self.img = clip(state_img_list, img_coord[0], img_coord[1],img_size[0], img_size[1])
        # self.img = state_img_list
        self.img = pygame.transform.scale(pygame.transform.flip(self.img, self.flip, False),
                                          (self.img.get_width() * self.scale, self.img.get_height() * self.scale))
        img_rect = self.img.get_rect()
        img_rect.center = (self.x, self.y)
        screen.blit(self.img, img_rect)
        self.index = (self.index + 1) % max_index

    def detect_collision(self):
        pass

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        if self.x < self.CENTER - 300:
            self.dx *= -1
            self.flip = True
        elif self.x > self.CENTER + 300:
            self.dx *= -1
            self.flip = False
