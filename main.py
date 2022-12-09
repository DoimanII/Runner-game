import random
import pygame as pg

import sys
from Settings import *
import engine as E

pg.init()
E.load_animation('data/assets/')

player = E.Entity('human', WIN_RES[0] // 2 - 6, WIN_RES[1] / 1.5, 13, 15)
ground.append(pg.Rect(0, 300, 500, 100))
StaminaHUD = E.Entity('StaminaHUD', 25, 25, 100, 25)
StaminaHUD.color = (62, 162, 201)

for x in range(1):
    falling_blocks.append(E.Entity('falling_block', 33 * x, -x * 100, 32, 300))
    if random.randint(0, 100) < 60:
        if random.randint(0, 100) < 50:
            ground.append(pg.Rect(WIN_RES[0] * x, 300 - 32, 32, 32))
        if random.randint(0, 100) > 50:
            ground.append(pg.Rect(WIN_RES[0] * x + 32, 300 - 32, 32, 32))
            ground.append(pg.Rect(WIN_RES[0] * x + 32, 300 - 64, 32, 32))
            ground.append(pg.Rect(WIN_RES[0] * x, 300 - 32, 32, 32))

dg = WIN_RES[0] // 100  # Это только для пола
db = WIN_RES[0] // 32
entity_chunks = {}
while True:
    # World generation
    for x in range(dg):
        t_x = x + round(camera[0] / 500) - 1
        if pg.Rect(t_x * 500, 300, 500, 100) not in ground:
            ground.append(pg.Rect(t_x * 500, 300, 500, 100))
    for x in range(db): # ЭТО НАДО ПЕРЕРАБОТАТЬ!
        chunk = x + round(camera[0] / (33))
        t_x = camera[0] + chunk * 33
        if chunk not in entity_chunks:
            entity_chunks[chunk] = t_x
            falling_blocks.append(E.Entity('falling_block', t_x, -x * 100, 32, 300))
        print(len(falling_blocks))
    camera[0] = player.get_pos()[0] - WIN_RES[0] // 2 + player.get_size()[0] // 2
    # Input
    if keys['right'] and can_input:
        player.flip_x = False
        player.action = 'walk'
        player_movement[0] = -3 * speed
    if keys['left'] and can_input:
        player.flip_x = True
        player.action = 'walk'
        player_movement[0] = 3 * speed
    if keys['up'] and can_input:
        if air_timer < 6:
            player_momentum = -6

    if keys['run'] and stamina >= 0 and (keys['left'] or keys['right']):
        stamina -= 2
        if stamina > 15:
            speed = 2.5
    elif not keys['run'] or stamina <= 0:
        speed = 1
        if stamina <= 100:
            stamina += 0.1
    StaminaHUD.set_size(stamina, 25)

    if not keys['right'] and not keys['left']:
        player.action = 'idle'
        player_movement[0] = 0
    # Player physics
    player_movement[1] = player_momentum
    tile_name, collision = player.obj.move(player_movement, ground, [])

    if collision['bottom'] or collision['top']:
        air_timer = 0
        player_momentum = 1
    else:
        air_timer += 1

    player_momentum += 0.5
    if player_momentum >= 6:
        player_momentum = 6
    # Render and another physic logic
    display.fill('grey')
    player.render(display, camera)
    momentum_fall += 1
    if momentum_fall > 10:
        momentum_fall = 10

    for falling_block in falling_blocks:  # Falling blocks render
        falling_block.render(display, camera)
        fal_tile_name, fal_collision = falling_block.obj.move([0, momentum_fall], ground, [player])
        if fal_tile_name['name'] == 'human':  # Здесь проблема!  #################
            can_input = False
            keys = {'up': False, 'down': False, 'right': False, 'left': False, 'run': False}

    for g in ground:  # Ground render
        if g.x - camera[0] < -1500:
            ground.remove(g)
        pg.draw.rect(display, 'darkgreen', (g.x - camera[0], g.y - camera[1], g.width, g.height))
    StaminaHUD.render(display)  # HUD render

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
            if event.key == pg.K_LSHIFT:
                keys['run'] = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_a:
                keys['right'] = False
            if event.key == pg.K_d:
                keys['left'] = False
            if event.key == pg.K_SPACE:
                keys['up'] = False
            if event.key == pg.K_LSHIFT:
                keys['run'] = False
