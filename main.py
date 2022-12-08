import random

import pygame as pg
import sys
from Settings import *
import engine as E

pg.init()
E.load_animation('data/assets/')

player = E.Entity('human', WIN_RES[0] // 2 - 6, WIN_RES[1] / 1.5, 13, 15)
ground.append(pg.Rect(0, 300, 500, 100))
for x in range(150):
    falling_blocks.append(E.Entity('falling_block', 33 * x, -x * 100, 32, 300))
dg = WIN_RES[0] // 100  # Это только для пола
db = WIN_RES[0] // 32

while True:

    for x in range(dg):
        t_x = x + round(camera[0] / 500) - 1
        if pg.Rect(t_x * 500, 300, 500, 100) not in ground:
            ground.append(pg.Rect(t_x * 500, 300, 500, 100))



    camera[0] = player.get_pos()[0] - WIN_RES[0] // 2 + player.get_size()[0] // 2

    if keys['right'] and can_input:
        player.flip_x = False
        player.action = 'walk'
        player_movement[0] = -3
    if keys['left'] and can_input:
        player.flip_x = True
        player.action = 'walk'
        player_movement[0] = 3
    if keys['up'] and can_input:
        if air_timer < 6:
            player_momentum = -6

    if not keys['right'] and not keys['left']:
        player.action = 'idle'
        player_movement[0] = 0

    player_movement[1] = player_momentum
    tile_name, collision = player.obj.move(player_movement, ground, falling_blocks)

    if collision['bottom'] or collision['top']:
        air_timer = 0
        player_momentum = 1
    else:
        air_timer += 1

    player_momentum += 0.5
    if player_momentum >= 6:
        player_momentum = 6

    display.fill('grey')
    player.render(display, camera)
    momentum_fall += 1
    if momentum_fall > 10:
        momentum_fall = 10

    for falling_block in falling_blocks:
        falling_block.render(display, camera)
        falling_block.obj.move([0, momentum_fall], ground, [player])

    for g in ground:
        if g.x-camera[0] < -1500:
            ground.remove(g)
        pg.draw.rect(display, 'darkgreen', (g.x - camera[0], g.y - camera[1], g.width, g.height))

    surf = pg.transform.scale(display, WIN_SIZE)
    screen.blit(surf, (0, 0))
    pg.display.flip()
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                keys['right'] = True
            if event.key == pg.K_d:
                keys['left'] = True
            if event.key == pg.K_SPACE:
                keys['up'] = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_a:
                keys['right'] = False
            if event.key == pg.K_d:
                keys['left'] = False
            if event.key == pg.K_SPACE:
                keys['up'] = False
