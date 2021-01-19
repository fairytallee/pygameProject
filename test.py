import pygame
from pygame import *
import math
import time


class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Images/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 4

        if self.rect.y > 520:
            BulletList.empty()


def main3():
    moveX = 0
    TrapList.empty()

    player.rect.x,player.rect.y = 50,0
    BulletList.add(bullet)
    FiringBullet = pygame.USEREVENT + 1
    pygame.time.set_timer(FiringBullet, 3000)

    GameExit = False

    while GameExit==False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-player.speed,0)
                if event.key == pygame.K_RIGHT:
                    player.move(player.speed,0)
                if event.key == pygame.K_UP:
                    player.move(0,-10)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.move(player.speed,0)
                if event.key == pygame.K_RIGHT:
                    player.move(-player.speed,0)
                if event.key == pygame.K_UP:
                    player.move(0,0)

            if event.type == FiringBullet:
                BulletList.add(bullet)
        print(BulletList)

        screen.fill(BLACK)
        level3.update()

        if player.rect.x > 350:
            for eachbullet in BulletList:
                BulletList.draw(screen)
                BulletList.update()


        playergroup.update()
        playergroup.draw(screen)

        player.Level3PlatColl(BlockListDirt2)
        pygame.display.update()
        clock.tick(60)
    bullet = Bullets(400,200)
    BulletList = pygame.sprite.Group()
main3()