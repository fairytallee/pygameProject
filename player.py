import pygame
from pygame import *
import math
import time

JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз

MOVE_SPEED = 7
WIDTH = 20
HEIGHT = 50
COLOR = "white"

sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()


class Bullet(sprite.Sprite):
    def __init__(self, x, y, speedx, click_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.time = None
        self.rect.x = x
        self.rect.y = y
        self.speedx = speedx
        self.click_pos = click_pos

    def update_bullet(self):
        if self.click_pos < self.rect.x:
            self.rect.x -= self.speedx
        if self.click_pos > self.rect.x:
            self.rect.x += self.speedx
        if pygame.time.get_ticks() - self.time >= 1500:
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
        self.speed = 1

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

    def Shoot(self, entity_group, click_pos):
        pos_x = click_pos[0]

        if pos_x != self.rect.centerx:
            bullet = Bullet(self.rect.centerx, self.rect.centery, 20, pos_x)
            bullet.time = pygame.time.get_ticks()
            entity_group.add(bullet)
            bullets.add(bullet)

        else:
            bullet = Bullet(self.rect.centerx, self.rect.centery, 0, pos_x)
            bullet.time = pygame.time.get_ticks()
            sprites.add(bullet)
            bullets.add(bullet)
