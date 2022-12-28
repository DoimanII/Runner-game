import random
import pygame as pg
import sys
from Settings import *
import engine as E

pg.init()
pg.display.set_caption('Runner by Doiman')
# Sounds load
pg.mixer.music.load('data/assets/sounds/Runner_bg_song_0 (mp3cut.net) (2).mp3')
pg.mixer.music.play(loops=-1)
jump_sound = pg.mixer.Sound('data/assets/sounds/jump-sound-beepbox_W04ybz0Z.mp3')
jump_sound.set_volume(0.2)
step_sound = [pg.mixer.Sound('data/assets/sounds/player-step-01_j6DIkTpi.mp3'), pg.mixer.Sound('data/assets/sounds/player-step-02_w7MNInX4.mp3')]
step_sound_timer = 0
for s in step_sound:
    s.set_volume(0.5)

E.load_animation('data/assets/')

player = E.Entity('human', 0, WIN_RES[1] / 1.5, 14, 30)

StaminaHUD = E.Entity('StaminaHUD', 25, 25, 100, 25)
StaminaHUD.color = (62, 162, 201)

while True:
    score = player.get_pos()[0]//32
    camera[0] = player.get_pos()[0] - WIN_RES[0] // 2 + player.get_size()[0] // 2
    display.fill('yellow')

    # Sounds
    if step_sound_timer > 0:
        step_sound_timer -= 1

    # World generation
    # Blocks
    bx = 3 + round(camera[0]/(32*5))
    if bx not in entity_chunks:
        entity_chunks[bx] = E.chunk_generation(bx*32*5,0 ,5, type='blockG')
        for pos in entity_chunks[bx]:
            entity.append(E.Entity('block', *pos, 32, 32,image=box_img))
    # Falling block
    if game_start:
        momentum_fall += 1
        if momentum_fall > 10:
            momentum_fall = 10
        fx =0 + round(camera[0]/(32*12))
        if fx not in falling_blocks_chunk:
            falling_blocks_chunk[fx] = E.chunk_generation(fx, 160, 12,'fal')
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
    if keys['right'] and can_input: # X-axis
        player.flip_x = True
        player.action = 'walk'
        player_movement[0] = -2 * speed
    if keys['left'] and can_input:
        player.flip_x = False
        player.action = 'walk'
        player_movement[0] = 2 * speed
    if keys['up'] and can_input: # Y-axis
        if air_timer < 6:
            player_momentum = -6
            jump_sound.play()
    #Stamina logic
    if keys['run'] and stamina >= 0 and (keys['left'] or keys['right']):
        stamina -= 2
        if stamina > 15:
            speed = 2.5
    elif not keys['run'] or stamina <= 0:
        speed = 1
        if stamina <= 100:
            stamina += 0.1
    StaminaHUD.set_size(stamina, 25)
    # Idle animation
    if not keys['right'] and not keys['left']:
        player.action = 'idle'
        player_movement[0] = 0

    # Player physics
    player_movement[1] = player_momentum
    tile_name, collision = player.obj.move(player_movement, ground, entity)


    if collision['bottom']:
        air_timer = 0
        player_momentum = 1
        if player_movement[0] != 0 and step_sound_timer == 0:
            step_sound_timer = 10
            random.choice(step_sound).play()
    else:
        air_timer += 1

    player_momentum += 0.5
    if player_momentum >= 6:
        player_momentum = 6

    # Render and another physic logic
    for ent in entity: # Entity
        if ent.get_pos()[0]-camera[0] <= -1000:
            entity.remove(ent)
        ent.render(display, camera)

    player.render(display, camera) # Player

    for falling_block in falling_blocks:  # Falling blocks render
        if falling_block.get_pos()[0]-camera[0] <= -1000:
            falling_blocks.remove(falling_block)
        falling_block.render(display, camera)
        fal_tile_name, fal_collision = falling_block.obj.move([0, momentum_fall], ground, [player])
        if fal_tile_name['name'] == 'human':  # Здесь проблема!  #################
            can_input = False
            keys = {'up': False, 'down': False, 'right': False, 'left': False, 'run': False}

    for g in ground:  # Ground render
        if g.x - camera[0] < -1500:
            ground.remove(g)
        display.blit(ground_img, (g.x - camera[0], g.y - camera[1], g.width, g.height))

    # HUD render
    StaminaHUD.render(display)  if can_input else None
    E.print_game_text(display, f'{score}м', (250, 25), 16)
    if not game_start:
        E.print_game_text(display, 'Press any button', (55, WIN_RES[1]//2),16, 'black')
        E.print_game_text(display, 'A D - идти', (55, WIN_RES[1] // 2+24), 8, 'black')
        E.print_game_text(display, 'SPACE - прыжок', (55, WIN_RES[1] // 2+36), 8, 'black')
        E.print_game_text(display, 'SHIFT - бежать', (55, WIN_RES[1] // 2+48), 8, 'black')
    if not can_input:
        E.print_game_text(display, 'Game over', (100, WIN_RES[1]//2),16, 'black')

    surf = pg.transform.scale(display, WIN_SIZE)
    screen.blit(surf, (0, 0))
    pg.display.flip()
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            game_start = True
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
