import os
import sys

from random import randint

import pygame
from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode((1000, 600))

pygame.display.set_caption('Arena')
x = 400
y = 250
x_c = 50
y_c = 25
width = 45
height = 40
speed = 10
img_a_d = pygame.image.load("walk_down.png")
img_a_l = pygame.image.load("walk_left.png")
img_a_u = pygame.image.load("walk_up.png")
img_a_r = pygame.image.load("walk_right.png")

MAXHEALTH = 10
PLAYER_IMG = pygame.image.load('player.png')
PLAYER_Trance = pygame.transform.scale(PLAYER_IMG, (width, height))

SCREENRECT = Rect(0, 0, 640, 480)
BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

wave = 0
wave_flg = False
first_flg = True
zombie_group = []


def quit():
    pygame.quit()
    sys.exit()


# Декор
class Decor(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.src_img = pygame.image.load(image)
        self.image = self.src_img
        self.rect = self.image.get_rect()
        self.rect.center = self.position

class Walls(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.src_img = pygame.image.load(image)
        self.image = self.src_img
        self.rect = self.position


side_brick = [Walls('side_brick.png', (0,i)) for i in range(0,601,64)]
side_brick2 = [Walls('side_brick.png', (968,i)) for i in range(0,601,64)]
wall_brick = [Walls('wall_brick.png', (i,0)) for i in range(0,1001,32)]
wall_brick2 = [Walls('wall_brick.png', (i,568)) for i in range(0,1001,32)]
mid_wall1 = Walls('side_wall.png', (389,0))
mid_wall2 = Walls('side_wall.png', (521,0))
side_wall1 = Walls('side_wall.png', (257,0))
side_wall2 = Walls('side_wall.png', (653,0))
timber_door = Walls('timber_door.png', (347,0))
timber_door2 = Walls('timber_door.png', (479,0))
timber_door3 = Walls('timber_door.png', (611,0))
corner_right = Walls('corner_right.png', (927,0))
corner_left = Walls('corner_left.png', (32,0))

grass1 = [Decor('grass1.png', (randint(50,950),randint(50,550))) for i in range(60)]
grass2 = [Decor('grass2.png', (randint(20,950),randint(20,550))) for i in range(10)]
grass3 = [Decor('grass3.png', (randint(30,650),randint(20,250))) for i in range(10)]
stone = [Decor('stone1.png', (randint(50,950),randint(50,550))) for i in range(20)]

decor_group = pygame.sprite.RenderPlain(grass1, grass2, grass3, stone)
walls_group = pygame.sprite.RenderPlain(wall_brick, side_brick, wall_brick2, side_brick2, mid_wall1, mid_wall2, side_wall1, side_wall2, timber_door, timber_door2, timber_door3, corner_right, corner_left)


#ПЕРСОНАЖ


class PlayerSprite(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.speed = self.direction = 0
        self.image = image
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.speed_x = 0
        self.speed_y = 0
        self.k_left = self.k_right = self.k_up = self.k_down = 0
        self.facing = RIGHT
        self.origtop = self.rect.top
        self.health = 10

    def update(self, direction, deltat):
        if direction:
            self.facing = direction
            self.speed_y = (self.k_up + self.k_down)
            self.speed_x = (self.k_left + self.k_right)
            x, y = self.position
            x += self.speed_x
            y += self.speed_y

        if x <= 50:
            x = 50
        if x >= 950:
            x = 950
        if y <= 50:
            y = 50
        if y >= 550:
            y = 550

        if y <= 258 and y >= 86 and x >= 190 and x <= 280:
            if x <= 200 or x >= 270:
                if x >= 220:
                    x = 280
                elif x <= 220:
                    x = 190
            if y <= 96 or y >= 248:
                if y >= 200:
                    y = 258
                elif y <= 200:
                    y = 86

            self.position = (x, y)
            self.rect = self.image.get_rect()
            self.rect.center = self.position


rect = screen.get_rect()
player = PlayerSprite(PLAYER_Trance, rect.center)
player_group = pygame.sprite.RenderPlain(player)


class Shot(pygame.sprite.Sprite):

    def __init__(self, image, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.position = (x, y)
        self.rect = self.position
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.direction = direction

    def update(self):

        if self.direction == "down":
            x, y = self.position
            x += 0
            y += 20
            self.position = (x, y)
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            if y >= 580:
                self.kill()

        if self.direction == "up":
            x, y = self.position
            x += 0
            y -= 20
            self.position = (x, y)
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            if y <= 10:
                self.kill()

        if self.direction == "left":
            x, y = self.position
            x -= 20
            y -= 0
            self.position = (x, y)
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            if x <= 0:
                self.kill()

        if self.direction == "right":
            x, y = self.position
            x += 20
            y -= 0
            self.position = (x, y)
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            if x >= 990:
                self.kill()


rect = screen.get_rect()
arrow_group_down = pygame.sprite.RenderPlain()

rect = screen.get_rect()
arrow_group_up = pygame.sprite.RenderPlain()

rect = screen.get_rect()
arrow_group_left = pygame.sprite.RenderPlain()

rect = screen.get_rect()
arrow_group_right = pygame.sprite.RenderPlain()


#миньоны
class MinionSprite(pygame.sprite.Sprite):
    def __init__(self, image, position, speed_lower, speed_upper, health):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.src_image = pygame.image.load(image)
        self.image = self.src_image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed_x = 0
        self.speed_y = 0
        self.speed_lower = speed_lower
        self.speed_upper = speed_upper
        self.health = health

    def update(self,deltat):
        if player.position[0] > self.position[0]:
            self.speed_x = randint(self.speed_lower, self.speed_upper)
        if player.position[0] < self.position[0]:
            self.speed_x = -randint(self.speed_lower, self.speed_upper)
        if player.position[1] > self.position[1]:
            self.speed_y = randint(self.speed_lower, self.speed_upper)
        if player.position[1] < self.position[1]:
            self.speed_y = -randint(self.speed_lower, self.speed_upper)

        x, y = self.position

        if y <= 258 and y >= 86 and x >= 180 and x <= 280:
            if x <= 190 or x >= 270:
                if x >= 220:
                    x = 280
                elif x <= 220:
                    x = 180
            if y <= 96 or y >= 248:
                if y >= 200:
                    y = 258
                elif y <= 200:
                    y = 86

        x += self.speed_x
        y += self.speed_y
        self.position = (x, y)
        self.rect.center = self.position
        if self.health <= 0:
                self.kill()


def message_to_screen(msg, color, x, y):
    screen_text = BASICFONT.render(msg, True, color)
    screen.blit(screen_text, [x, y])


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def coverscreen():
    coverscreen = True
    filename = "cover_2.png"
    while coverscreen:
        BackGround = Background(filename, [0,0])
        screen.blit(BackGround.image, BackGround.rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
                 quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    coverscreen = False


def drawHealthBar(currentHealth):
    for i in range(int(currentHealth)):
        pygame.draw.rect(screen, (255, 0, 0),   (30, 5 + (10 * MAXHEALTH) - i * 10, 20, 10))
    for i in range(MAXHEALTH):
        pygame.draw.rect(screen, (255, 255, 255), (30, 5 + (10 * MAXHEALTH) - i * 10, 20, 10), 1)


run = True
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

minion_group = []
total = 11
coverscreen()

first_flg_up = True
first_flg_down = True
first_flg_left = True
first_flg_right = True
first_flg_left2 = True
first_flg_right2 = True

game_end = False
game_over = False

player.health = MAXHEALTH
player.position = (500, 300)
deltat = clock.tick(25)

while not game_end:
    # message_to_screen(("Волнa:" + str(wave)), (255, 255, 255), 850, 40)
    #  pygame.display.update()
    #while game_over:
    #    message_to_screen(" Game Over Нажмите [Q] чтобы выйти", (255, 255, 255), 300, 250)
    #    pygame.display.update()
    #    for event in pygame.event.get():
    #        if event.type == KEYDOWN:
    #            if event.key == pygame.K_q:
    #                game_over = False
    #                game_end = True
    #                pygame.quit()
    #                quit()

    for event in pygame.event.get():
        if not hasattr(event, 'key'):
            continue
        down = event.type == KEYDOWN
        if event.key in (K_RIGHT, K_d):
            player.k_right = down * randint(4, 6)
        elif event.key in (K_LEFT, K_a):
            player.k_left = down * -randint(4, 6)
        elif event.key in (K_UP, K_w):
            player.k_up = down * -randint(4, 6)
        elif event.key in (K_DOWN, K_s):
            player.k_down = down * randint(4, 6)

        elif event.key == K_j:
            if first_flg_down == True:
                arrow_down = Shot('arrow_down.png', player.position[0], player.position[1], "down")
                arrow_group_down.add(arrow_down)
                first_flg_down = False
                last_down = pygame.time.get_ticks()
            else:
                now_down = pygame.time.get_ticks()
                if last_down - now_down <= -300:
                    arrow_down = Shot('arrow_down.png', player.position[0], player.position[1], "down")
                    arrow_group_down.add(arrow_down)
                    last_down = pygame.time.get_ticks()

        elif event.key == K_u:
            if first_flg_up == True:
                arrow_up = Shot('arrow_up.png', player.position[0], player.position[1], "up")
                arrow_group_up.add(arrow_up)
                first_flg_up = False
                last_up = pygame.time.get_ticks()
            else:
                now_up = pygame.time.get_ticks()
                if last_up - now_up <= -300:
                    arrow_up = Shot('arrow_up.png', player.position[0], player.position[1], "up")
                    arrow_group_up.add(arrow_up)
                    last_up = pygame.time.get_ticks()

        elif event.key == K_h:
            if first_flg_left == True:
                arrow_left = Shot('arrow_left.png', player.position[0], player.position[1], "left")
                arrow_group_left.add(arrow_left)
                first_flg_left = False
                last_left = pygame.time.get_ticks()
            else:
                now_left = pygame.time.get_ticks()
                if last_left - now_left <= -300:
                    arrow_left = Shot('arrow_left.png', player.position[0], player.position[1], "left")
                    arrow_group_left.add(arrow_left)
                    last_left = pygame.time.get_ticks()

        elif event.key == K_k:
            if first_flg_right == True:
                arrow_right = Shot('arrow_right.png', player.position[0], player.position[1], "right")
                arrow_group_right.add(arrow_right)
                first_flg_right = False
                last_right = pygame.time.get_ticks()
            else:
                now_right = pygame.time.get_ticks()
                if last_right - now_right <= -300:
                    arrow_right = Shot('arrow_right.png', player.position[0], player.position[1], "right")
                    arrow_group_right.add(arrow_right)
                    last_right = pygame.time.get_ticks()
        elif event.key == K_ESCAPE:
            quit()

    if first_flg == True:
        zombie = [MinionSprite("zombie_resize.png", (495, 0), -2, 3, 10) for i in range(1)]
        zombies = pygame.sprite.Group(zombie)
        zombie_group = pygame.sprite.RenderPlain(zombies)
        minion_group.append(zombies)

        rand_zombie = [MinionSprite("zombie_resize.png", (495, 0), -2, 3, 10) for i in range(1)]
        rand_zombies = pygame.sprite.Group(rand_zombie)
        rand_zombie_group = pygame.sprite.RenderPlain(rand_zombies)
        minion_group.append(zombies)

        max_health = [Decor('max_health.png', (randint(20, 950), randint(20, 550))) for i in range(0)]
        max_healths = pygame.sprite.Group(max_health)
        max_health_group = pygame.sprite.RenderPlain(max_healths)

        last_zombie = pygame.time.get_ticks()
        last_max_health = pygame.time.get_ticks()
        first_flg = False
        wave += 1
    now_max_health = pygame.time.get_ticks()

    if now_max_health - last_max_health >= 4000:
        max_health = [Decor('max_health.png', (randint(20, 950), randint(20, 550))) for i in range(1)]
        max_healths.add(max_health)
        max_health_group = pygame.sprite.RenderPlain(max_healths)
        last_max_health = pygame.time.get_ticks()
    now_zombie = pygame.time.get_ticks()

    if now_zombie - last_zombie >= 5000:
        rand_zombie = [MinionSprite('zombie_resize.png', (randint(30, 970), randint(30, 570)), -2, 3, 10) for i in
                       range(wave // 2)]
        rand_zombies.add(rand_zombie)
        rand_zombie_group = pygame.sprite.RenderPlain(rand_zombies)
        minion_group.append(rand_zombies)
        last_zombie = pygame.time.get_ticks()

    if len(zombies) == 0 and wave in range(1, 3):
        zombie = [MinionSprite('zombie_resize.png', (495, 0), -2, 3, 10) for i in range(2 * wave)]
        zombies = pygame.sprite.Group(zombie)
        zombie_group = pygame.sprite.RenderPlain(zombies)
        minion_group.append(zombies)
        wave += 1
        wave_flg = False

    screen.fill((139, 195, 73))
    walls_group.draw(screen)
    drawHealthBar(player.health)
    decor_group.draw(screen)

    player_group.update(LEFT, deltat)
    player_group.draw(screen)

    zombie_group.update(deltat)
    zombie_group.draw(screen)

    rand_zombie_group.update(deltat)
    rand_zombie_group.draw(screen)

    arrow_group_down.update()
    arrow_group_down.draw(screen)

    arrow_group_up.update()
    arrow_group_up.draw(screen)

    arrow_group_left.update()
    arrow_group_left.draw(screen)

    arrow_group_right.update()
    arrow_group_right.draw(screen)

    max_health_group.draw(screen)
    max_health_group.update()

    pygame.display.flip()

    for zombie in pygame.sprite.spritecollide(player, zombies, False):
        player.health -= 0.1
    for rand_zombie in pygame.sprite.spritecollide(player, rand_zombies, False):
        player.health -= 0.1
    for max_health in pygame.sprite.spritecollide(player, max_healths, False):
        if player.health != 10:
            player.health = MAXHEALTH
            max_health.kill()

    if player.health <= 0:
        game_over = True
    if minion_group == []:
        game_over = True

    for i in range(len(minion_group)):
        for minion in minion_group[i]:
            minion.health -= 3 * len(pygame.sprite.spritecollide(minion, arrow_group_down, True))
        for minion in minion_group[i]:
            minion.health -= 3 * len(pygame.sprite.spritecollide(minion, arrow_group_up, True))
        for minion in minion_group[i]:
            minion.health -= 3 * len(pygame.sprite.spritecollide(minion, arrow_group_right, True))
        for minion in minion_group[i]:
            minion.health -= 3 * len(pygame.sprite.spritecollide(minion, arrow_group_left, True))

    if player.health <= 0:
        player.kill()
pygame.quit()

quit()