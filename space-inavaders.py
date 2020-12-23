import pygame as pg
import random as rd
import math
from pygame import mixer
from pygame import sprite
from pygame import rect
from pygame.locals import *
import time

# init
pg.init()
clock = pg.time.Clock()
sc = pg.display.set_mode((600, 600))
pg.display.set_caption("infinity shot")
MP3 = "C:/Users/User/Desktop/python projects/shoting/"
IMG = "C:/Users/User/Desktop/python/"
had_fireshoted = pg.time.get_ticks()
red = (255, 0, 0)
gr = (0, 255, 0)
lg = pg.image.load(IMG + "lg1.png")

back_s = pg.mixer.Sound(MP3 + "bcsound1.mp3")
back_s.set_volume(0.10)

ship_shot = pg.mixer.Sound(MP3 + "shot1.mp3")
ship_shot.set_volume(0.25)

exp_S = pg.mixer.Sound(MP3 + "expl.wav")
exp_S.set_volume(0.25)

# load images player
back_gr = pg.image.load(IMG + "space.png")

T_font3 = pg.font.SysFont("consolas", 60)
T_font4 = pg.font.SysFont("consolas", 60)
lose = 0
timer = 3
last_count = pg.time.get_ticks()


def show():
    sc.blit(back_gr, (0, 0))


def start_end(text, font, text_col, x, y):
    form = font.render(text, True, text_col)
    sc.blit(form, (x, y))


class Ship(pg.sprite.Sprite):
    def __init__(self, x, y, HP):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(IMG + "ship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.HP_F = HP
        self.HP_fin = HP
        self.had_shoted = pg.time.get_ticks()

    def update(self):
        lose = 0
        key = pg.key.get_pressed()
        if key[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if key[pg.K_RIGHT] and self.rect.right < 600:
            self.rect.x += 5

        just_shoted = pg.time.get_ticks()
        if key[pg.K_SPACE] and just_shoted-self.had_shoted > 300:
            ship_shot.play()
            bullet = Bullet(self.rect.centerx, self.rect.top)
            Bullet_G.add(bullet)   
            self.had_shoted = just_shoted

        self.mask = pg.mask.from_surface(self.image)

        pg.draw.rect(sc, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.HP_fin > 0:
            pg.draw.rect(sc, gr, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.HP_fin / self.HP_F)), 15))
        elif self.HP_fin <= 0:
            self.kill()
            expl = EXP(self.rect.centerx, self.rect.centery, 3)
            exp_G.add(expl)
            lose = -1
        return lose


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(IMG + "bullets.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 5
        if self.rect.top < 0:
            self.kill()
        if pg.sprite.spritecollide(self, Enemies_G, True):
            self.kill()
            exp_S.play()
            expl = EXP(self.rect.centerx, self.rect.centery, 2)
            exp_G.add(expl)


class Enemies(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(IMG + "mn"+str(rd.randint(2, 5))+".png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.move_c = 0
        self.move_d = 1

    def update(self):
        self.rect.x += self.move_d
        self.move_c += 1
        if abs(self.move_c) > 55:
            self.move_d *= -1
            self.move_c *= self.move_d


class Enemies_B(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(IMG + "fire.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        lose = 0
        self.rect.y += 2
        if self.rect.top > 600:
            self.kill()
        if pg.sprite.spritecollide(self, SH_G, False, pg.sprite.collide_mask):
            self.kill()
            ship.HP_fin -= 1
            exp_S.play()
            expl = EXP(self.rect.centerx, self.rect.centery, 5)
            exp_G.add(expl)


class EXP(pg.sprite.Sprite):
    def __init__(self, x, y, size):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        for k in range(1, 3):
            img = pg.image.load(IMG + F"exp{k}.png")
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= 3 and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= 3:
            self.kill()

ship = Ship(300, 500, 3)
SH_G = pg.sprite.Group()
Bullet_G = pg.sprite.Group()
Enemies_G = pg.sprite.Group()
enemy_bullet_G = pg.sprite.Group()
exp_G = pg.sprite.Group()
SH_G.add(ship)


def quantity():
    for i in range(5):
        for j in range(10):
            enemy = Enemies(80+j*50, 80+i*50)
            Enemies_G.add(enemy)
quantity()

def logo():
    sc.blit(lg, (70, 90))


running = True
while running:
    clock.tick(60)
    show()

    if timer == 0:

        just_shoted = pg.time.get_ticks()
        if just_shoted - had_fireshoted > 100 and len(enemy_bullet_G) < 8:
            ST_SH = rd.choice(Enemies_G. sprites())
            enemies_b = Enemies_B(ST_SH.rect.centerx, ST_SH.rect.bottom)
            enemy_bullet_G.add(enemies_b)
            had_fireshoted = just_shoted

        if len(Enemies_G) == 0:
            lose = 1

        if lose == 0:
            lose = ship.update()
            Bullet_G.update()
            Enemies_G.update()
            enemy_bullet_G.update()
        else:
            if lose == -1:
                start_end("Game Over", T_font4, red, 150, 350)
            if lose == 1:
                logo()
                start_end("You win!", T_font4, red, 150, 10)

    if timer > 0:
        start_end("Get ready!", T_font4, (255, 255, 255), 150, 350)
        start_end(str(timer), T_font3, red, 280, 400)
        c_timer = pg.time.get_ticks()
        if c_timer - last_count > 1000:
            timer -= 1
            last_count = c_timer

    exp_G.update()
    SH_G.draw(sc)
    Bullet_G.draw(sc)
    Enemies_G.draw(sc)
    enemy_bullet_G.draw(sc)
    exp_G.draw(sc)
    # back_s.play()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
pg.quit()
