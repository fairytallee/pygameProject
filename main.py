import pygame
from pygame import *
import os
import time
from player import Player

WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
size = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную

pygame.init()  # Инициация PyGame, обязательная строчка
screen = pygame.display.set_mode(size)  # Создаем окошко
screen.fill('black')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удается загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 800, 640)


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group, group2):
        super().__init__(group, group2)
        self.rect = None


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(PLATFORM_WIDTH * pos_x, PLATFORM_HEIGHT * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                new_player = Player(PLATFORM_WIDTH * (x - 1), PLATFORM_HEIGHT * y)
                ll = list(level[y])
                ll[x] = '.'
                level[y] = ll
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


# Объявляем переменные
FPS = 60

PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 80
PLATFORM_COLOR = "black"
BACKGROUND_COLOR = "white"


tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('grass.png')
}

tiles_group = SpriteGroup()
all_sprites = SpriteGroup()
entity_group = SpriteGroup()

level_map = load_level('map.map')

hero, max_x, max_y = generate_level(level_map)
entity_group.add(hero)

clock = pygame.time.Clock()

left = False
right = False
up = False


def main():
    global left, right, up
    pygame.display.set_caption("test")
    # будем использовать как фо

    running = True

    while running:  # Основной цикл программы
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True

            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False

            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True

            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False

            if event.type == KEYDOWN and event.key == K_UP:
                up = True

            if event.type == KEYUP and event.key == K_UP:
                up = False

        screen.fill('black')
        all_sprites.draw(screen)
        entity_group.draw(screen)
        hero.update(left, right, up, tiles_group)
        entity_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()