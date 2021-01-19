import pygame
from pygame import *
import os


from player import Player
from player import Bullet
from Enemies import Enemy


WIN_WIDTH, WIN_HEIGHT = 1920, 1080
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
        self.rect = (0, 0, 1920, 1080)


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
    new_player, new_enemy, x, y = None, None, None, None
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
            elif level[y][x] == 'e':
                new_enemy = Enemy(PLATFORM_WIDTH * (x - 1), PLATFORM_HEIGHT * y)
                enemy_group.add(new_enemy)

    # вернем игрока, а также размер поля в клетках
    return new_player, new_enemy, x, y


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    # l = min(0, l)  # Не движемся дальше левой границы
    # l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    # t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    # t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


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
bullet_group = SpriteGroup()
enemy_group = SpriteGroup()

level_map = load_level('map.map')

hero, enemy, max_x, max_y = generate_level(level_map)
entity_group.add(hero)
entity_group.add(enemy)

total_level_width = (max_x + 1) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
total_level_height = (max_y + 1) * PLATFORM_HEIGHT  # высоту

camera = Camera(camera_configure, total_level_width, total_level_height)

clock = pygame.time.Clock()
left = False
right = False
up = False

camera.update(hero)


def menu_pause(screen):

    sur = pygame.Surface((500, 600))
    sur.fill((150, 150, 150, 100))
    screen.blit(sur, ((WIN_WIDTH // 2) - 250, (WIN_HEIGHT // 2) - 300))
    # pygame.draw.rect(screen, (207, 207, 207, 127), ((WIN_WIDTH // 2) - 250, (WIN_HEIGHT // 2) - 250, 500, 500))500

    pause_text = ["Не боись, это меню паузы", "Тыкни пробел"]
    font = pygame.font.Font(None, 50)
    offset_down = 0
    for line in pause_text:
        text = font.render(line, True, (255, 255, 255, 1))
        text_x = WIN_WIDTH // 2 - text.get_width() // 2
        text_y = ((WIN_HEIGHT // 2 - text.get_height() // 2) - 250) + offset_down
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        offset_down += 50


def main():
    global left, right, up, hero, enemy
    pygame.display.set_caption("test")

    running, pause, process = 1, 0, True
    state = running

    while process:  # Основной цикл программы
        if state == running:
            for event in pygame.event.get():  # Обрабатываем события
                if event.type == QUIT:
                    process = False

                if event.type == KEYDOWN and event.key == K_a:
                    left = True
                if event.type == KEYUP and event.key == K_a:
                    left = False

                if event.type == KEYDOWN and event.key == K_d:
                    right = True
                if event.type == KEYUP and event.key == K_d:
                    right = False

                if event.type == KEYDOWN and (event.key == K_w or event.key == K_SPACE):
                    up = True
                if event.type == KEYUP and (event.key == K_w or event.key == K_SPACE):
                    up = False

                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    state = pause
                    up = False
                    left = False
                    right = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        hero.Shoot(entity_group, event.pos)

            screen.fill('black')

            camera.update(hero)

            for spr in all_sprites:
                screen.blit(spr.image, camera.apply(spr))
            for e in entity_group:
                screen.blit(e.image, camera.apply(e))
            for bul in entity_group:
                if isinstance(bul, Bullet):
                    bul.update_bullet()
            hits = sprite.spritecollide(hero, enemy_group, True)
            if hits:
                process = False

            hero.update(left, right, up, tiles_group)
            enemy.update(tiles_group)

        elif state == pause:
            for event in pygame.event.get():  # Обрабатываем события
                if event.type == QUIT:
                    process = False
                if event.type == KEYDOWN and event.key == K_SPACE:
                    state = running
                    # screen.fill('black')

            menu_pause(screen)

        clock.tick(FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
