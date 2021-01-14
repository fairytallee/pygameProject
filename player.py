import pygame
from pygame import *
import math
import time

WIN_WIDTH, WIN_HEIGHT = 800, 600

JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз

MOVE_SPEED = 7
WIDTH = 20
HEIGHT = 50
COLOR = "white"

sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()


class Bullet(sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.x0 = x
        self.y0 = y
        self.rect.x = x
        self.rect.y = y
        self.speedx = speedx
        self.speedy = speedy

    def update_bullet(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.x - self.x0 == 3000 or self.x0 - self.rect.x == 3000\
                or self.rect.y - self.y0 == 3000 or self.y0 - self.rect.y == 3000:
            self.kill()


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)

        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?

        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.pos = (self.rect.x, self.rect.y)
        self.speed = 5

    def update(self, left, right, up, platforms):
        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n

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

    def Shoot(self, entity_group, pos_mouse_x, pos_mouse_y):

        if pos_mouse_x != self.rect.centerx or pos_mouse_y != self.rect.centery:

            self.a = pos_mouse_x - self.rect.centerx
            self.b = pos_mouse_y - self.rect.centery

            fTime = pos_mouse_x // self.speed

            speed_x = self.speed
            speed_y = self.b // fTime
            # self.a = pos_mouse_x - self.rect.centerx
            # self.b = self.rect.centery - pos_mouse_y
            # self.c = math.hypot(self.a, self.b)
            # self.t = self.c / self.speed
            # speed_x = self.a / self.t
            # speed_y = -self.b / self.t

            speed_x, speed_y = self.find_speed(pos_mouse_x, pos_mouse_y)

            bullet = Bullet(self.rect.centerx, self.rect.centery, speed_x, speed_y)
            entity_group.add(bullet)
            bullets.add(bullet)

        else:
            bullet = Bullet(self.rect.centerx, self.rect.centery, 0, 50)
            sprites.add(bullet)
            bullets.add(bullet)

    def find_speed(self, pos_mouse_x, pos_mouse_y):

        x = WIN_WIDTH // 2
        y = WIN_HEIGHT // 2

        a = abs(pos_mouse_x - x)
        b = abs(pos_mouse_y - y)
        c = math.sqrt(math.pow(a, 2) + math.pow(b, 2))

        count = c // self.speed

        if y < pos_mouse_y:
            speed_y = b // count
        elif y == pos_mouse_y:
            speed_y = 0
        else:
            speed_y = -(b // count)

        if x < pos_mouse_x:
            speed_x = a // count
        elif x == pos_mouse_x:
            speed_x = 0
        else:
            speed_x = -(a // count)

        return speed_x, speed_y
