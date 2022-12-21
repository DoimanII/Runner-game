import random
import pygame as pg

import sys
from Settings import *
import engine as E

pg.init()
E.load_animation('data/assets/')


player = E.Entity('human', 0, WIN_RES[1] / 1.5, 26, 30)

StaminaHUD = E.Entity('StaminaHUD', 25, 25, 100, 25)
StaminaHUD.color = (62, 162, 201)
for x in range(6,0,-1):
    falling_blocks.append(E.Entity('falling_block', 32 * -x, -100 - x*160, 32, 300, image=f_img[random.choice([0,1])]))
entity.append(E.Entity('block', 160, 160, 32, 32))

while True:
    camera[0] = player.get_pos()[0] - WIN_RES[0] // 2 + player.get_size()[0] // 2
    display.fill('yellow')
    # World generation
    # Blocks
    bx = 3 + round(camera[0]/(32*5))
    if bx not in entity_chunks:
        entity_chunks[bx] = E.chunk_generation(bx, 5, 'block')
        for pos in entity_chunks[bx]:
            entity.append(E.Entity('block', *pos, 32, 32))
            print(pos, player.get_pos())
    # Falling block
    fx = 0 + round(camera[0]/(32*12))
    if fx not in falling_blocks_chunk:
        falling_blocks_chunk[fx] = E.chunk_generation(fx, 12)
        for pos in falling_blocks_chunk[fx]:
            falling_blocks.append(E.Entity('falling_block', pos[0], -1000-pos[1], 32, 300, image=f_img[random.choice([0,1])]))

    # BackGround and ground
    for x in range(ds):
        chunk_bg = x - 1 + round(camera[0]/(320))
        if chunk_bg not in back_ground: # BackGround
            back_ground[chunk_bg] = [[320*chunk_bg,0],random.choice([0,0,0,1])]
        if chunk_bg not in ground_chunks: # Ground
            ground_chunks[chunk_bg] = [pg.Rect(chunk_bg*320, 190, 320, 10), 0]
            if ground_chunks[chunk_bg][0] not in ground:
                ground.append(ground_chunks[chunk_bg][0])
        display.blit(back_ground_img[back_ground[chunk_bg][1]], (back_ground[chunk_bg][0][0]-camera[0], back_ground[chunk_bg][0][1]-camera[1]))

    # Input
    if keys['right'] and can_input:
        player.flip_x = False
        player.action = 'walk'
        player_movement[0] = -2 * speed
    if keys['left'] and can_input:
        player.flip_x = True
        player.action = 'walk'
        player_movement[0] = 2 * speed
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
    tile_name, collision = player.obj.move(player_movement, ground, entity)

    if collision['bottom'] or collision['top']:
        air_timer = 0
        player_momentum = 1
    else:
        air_timer += 1

    player_momentum += 0.5
    if player_momentum >= 6:
        player_momentum = 6
    # Render and another physic logic

    for ent in entity:
        ent.render(display, camera)
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
        display.blit(ground_img, (g.x - camera[0], g.y - camera[1], g.width, g.height))
    StaminaHUD.render(display)  if can_input else None # HUD render

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
