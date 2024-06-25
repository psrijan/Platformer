import csv
from enum import Enum
from player import Soldier
from enemy import Enemy
from items import ItemBox, ItemBoxType, Water, Obstacle, Decoration
from state import GameState
import pygame

class TileType(Enum):
    EMPTY = -1
    GROUND = 0
    PLAYER = 15
    ENEMY = 16
    AMMO_BOX = 17
    GRANADE_BOX = 18
    HEALTH_BOX = 19
    NEXT_LEVEL = 20

class Level(object):
    def __init__(self, level=1, rowSize = 32, colSize = 32):
        self.cur_level = level
        #self.pygame = pygame
        self.img_list = []
        self.row_size = 32
        self.col_size = 32
        self.obstacle_list = []

        """
        for i in range(1, 6):
            img = pygame.image.load(f"./assets/levels/one/plx-{i}.png").convert_alpha()
            self.img_list.append(img)
        """

    def load_level_data(self, level_value):

        level_data = []
        for index in range(0, 16):
            level_data.append([-1] * 50)

        with open(f'assets/level_data/csvfiles/level-{level_value}.csv', 'r') as level_file:
            csv_reader = csv.reader(level_file)
            for rDx, row in enumerate(csv_reader):
                for cDx, col in enumerate(row):
                    level_data[rDx][cDx] = int(col)
        print(level_data)
        return level_data
    def process_level_data(self, level_data, state: GameState):
        player, enemy = None, None
        item_box_group = state.item_box_group
        enemy_group = state.enemy_group
        water_group = state.water_group
        obstacle_group = state.obstacle_group
        decoration_group = state.decoration_group

        for i in range(len(level_data)):
            for j in range(len(level_data[0])):
                val = level_data[i][j]

                if val == TileType.EMPTY.value:
                    pass
                elif val >= 0 and val <= 8:
                    # for ground
                    block = Obstacle(str(val),
                                  j * self.row_size, i * self.row_size)
                    obstacle_group.add(block)
                elif val >= 9 and val <= 10:
                    print("blitting water")
                    water = Water(str(val), j * self.row_size, i * self.row_size)
                    water_group.add(water)
                elif val == TileType.PLAYER.value:
                    print('creating player ')
                    player = Soldier(i * self.row_size, j * self.col_size, .25)
                elif val == TileType.PLAYER.value:
                    decoration = Decoration(str(val), j * self.row_size, i * self.row_size)
                    decoration_group.add(decoration)
                elif val == TileType.ENEMY.value:
                    enemy = Enemy(i * self.row_size, j * self.col_size, 1)
                    enemy_group.add(enemy)
                elif val == TileType.AMMO_BOX.value:
                    ammo = ItemBox(i * self.row_size, j * self.col_size, ItemBoxType.GUN)
                    item_box_group.add(ammo)
                elif val == TileType.GRANADE_BOX.value:
                    bomb = ItemBox(i * self.row_size, j * self.col_size, ItemBoxType.BOMB)
                    item_box_group.add(bomb)
                elif val == TileType.HEALTH_BOX.value:
                    health = ItemBox(i * self.row_size, j * self.col_size, ItemBoxType.HEART)
                    item_box_group.add(health)
        return player

    def refresh_screen(self, screen, state: GameState):
        screen.fill((0, 0, 0))
        state.obstacle_group.draw(screen)
        state.decoration_group.draw(screen)
        state.water_group.draw(screen)
        state.item_box_group.draw(screen)



    def create_background(self, level, scroll):
        #screen.blit((0,0,0))
        speed = 1
        for x in range(0, 4):
            for i in range(0, len(self.img_list)):
                img = self.img_list[i]
                screen.blit(img, (x * img.get_width() + scroll * speed, 0))
                speed += .2



if __name__ == "__main__":
    level = Level()
    level.load_level_data(0)