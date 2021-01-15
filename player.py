import pygame
from pygame import *
import math
import time

# WIN_WIDTH, WIN_HEIGHT = 700, 700
WIN_WIDTH, WIN_HEIGHT = 1920, 1080

JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз

HERO_MOVE_SPEED = 7
HERO_WIDTH = 20
HERO_HEIGHT = 50

BULLET_SIZE = 10
BULLET_SPEED = 20

COLOR = "white"

sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()


class Bullet(sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.x0 = x
        self.y0 = y
        self.rect.x = x
        self.rect.y = y
        self.speedx = speedx
        self.speedy = speedy

    def collide(self, platforms):
        pass
        for p in platforms:
            if sprite.collide_rect(self, p):
                self.kill()

    def update_bullet(self, platforms):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        self.collide(platforms)

        if self.rect.x - self.x0 == 3000 or self.x0 - self.rect.x == 3000 \
                or self.rect.y - self.y0 == 3000 or self.y0 - self.rect.y == 3000:
            self.kill()


def find_speed(pos_mouse_x, pos_mouse_y):

    x = WIN_WIDTH // 2
    y = WIN_HEIGHT // 2 + 20

    angel = math.radians(abs(math.degrees(math.atan2(abs(pos_mouse_x - x), abs(y - pos_mouse_y))) - 90))

    print(f"hero x: {x} y: {y}")
    print(f'angel: {math.degrees(angel)} degrees')
    print(f"mouse: x: {pos_mouse_x} y: {pos_mouse_y}")
    print()

    speed_x, speed_y = 0, 0

    if x < pos_mouse_x and y > pos_mouse_y:
        speed_x = math.cos(angel) * BULLET_SPEED
        speed_y = -(math.sin(angel)) * BULLET_SPEED
    elif x > pos_mouse_x and y > pos_mouse_y:
        speed_x = -(math.cos(angel) * BULLET_SPEED)
        speed_y = -(math.sin(angel) * BULLET_SPEED)
    elif x > pos_mouse_x and y < pos_mouse_y:
        speed_x = -(math.cos(angel) * BULLET_SPEED)
        speed_y = math.sin(angel) * BULLET_SPEED
    elif x < pos_mouse_x and y < pos_mouse_y:
        speed_x = math.cos(angel) * BULLET_SPEED
        speed_y = math.sin(angel) * BULLET_SPEED
    elif x == pos_mouse_x:
        speed_x = 0
        if y > pos_mouse_y:
            speed_y = -BULLET_SPEED
        elif y < pos_mouse_y:
            speed_y = BULLET_SPEED
        else:
            speed_y = BULLET_SPEED
    elif y == pos_mouse_y:
        speed_y = 0
        if x > pos_mouse_x:
            speed_x = -BULLET_SPEED
        elif x < pos_mouse_x:
            speed_x = BULLET_SPEED
        else:
            speed_x = 0
            speed_y = BULLET_SPEED

    return speed_x, speed_y


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)

        self.onGround = False  # На земле ли я?

        self.yvel = 0  # скорость вертикального перемещения
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте

        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y

        self.image = Surface((HERO_WIDTH, HERO_HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, HERO_WIDTH, HERO_HEIGHT)
        self.pos = (self.rect.x, self.rect.y)

        self.bullet_speed = 20

    def update(self, left, right, up, platforms):
        if left:
            self.xvel = -HERO_MOVE_SPEED  # Лево = x- n

        if right:
            self.xvel = HERO_MOVE_SPEED  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает

    def shoot(self, entity_group, pos_mouse_x, pos_mouse_y):

        speed_x, speed_y = find_speed(pos_mouse_x, pos_mouse_y)

        bullet = Bullet(self.rect.centerx - (BULLET_SIZE // 2),
                        self.rect.centery - (BULLET_SIZE // 2), speed_x, speed_y)
        entity_group.add(bullet)
        bullets.add(bullet)
