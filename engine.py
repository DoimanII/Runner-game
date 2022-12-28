import random

import pygame as pg
from Settings import *

def print_game_text(display, text, pos, text_size, color=(255,255,255)):
    font = pg.font.Font('data/assets/F77 Minecraft.ttf', text_size)
    img = font.render(str(text), False, color)
    display.blit(img, pos)
def get_mouse_pos():
    return (pg.mouse.get_pos()[0] // 2, pg.mouse.get_pos()[1] // 2)


def chunk_generation(x, y=160, chunk_size=0, type='fal'):
    chunk_data = []
    if type == 'fal':
        for x_pos in range(int(chunk_size)):
            t_x = (x * chunk_size + x_pos) * 32  # 32 !!!
            t_y = y*x_pos
            chunk_data.append((t_x, t_y))
    if type == 'block':
        for x_pos in range(int(chunk_size)):
            if random.choice([0,0,1,0]) == 1: # Лучше заранее написать все варианты структур, а не вот это вот все..
                t_x = (x * chunk_size + x_pos)*32
                t_y = random.choice([160, 120])
                chunk_data.append((t_x, t_y))
    if type == 'blockG':
        structure_type = random.choice([0,0,0,1,1,0,2,0,3,0,4,5])
        for y_inx, structure  in enumerate(structures[structure_type]):
            for x_inx, block in enumerate(structure):
                if block == 'B':
                    t_x = (x+int(chunk_size)*32) + x_inx*32
                    t_y = y + y_inx*32
                    chunk_data.append((t_x, t_y))
    return chunk_data


def load_animation(path):
    global animation_higher_database
    with open(path + 'entity_animation.txt', 'r') as f:
        data = f.read()
    for animation in data.split('\n'):
        sections = animation.split(' ')

        animation_info = sections[0].split('/')
        entity_name = animation_info[1]
        animation_name = animation_info[-1]
        if entity_name not in animation_higher_database:
            animation_higher_database[entity_name] = {}
        if animation_name not in animation_higher_database[entity_name]:
            animation_higher_database[entity_name][animation_name] = []
        frame_duration = sections[1].split(';')
        n = 0
        for frame in frame_duration:
            animation_path = path + sections[0] + '/' + animation_name + '_' + str(n) + '.png'
            animation_database[animation_path] = pg.transform.scale2x(pg.image.load(animation_path)).convert_alpha()
            for i in range(int(frame)):
                animation_higher_database[entity_name][animation_name].append(animation_path)
            n += 1


class physics():
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)

    def __test_collide(self, tiles, entities):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append([tile, 'tile', 0])
        for entity in entities:
            if self.rect.colliderect(entity.obj.rect):
                hit_list.append([entity.obj.rect, entity.name, entity.id])
        return hit_list

    def move(self, movement, tiles, entities):
        tile_name = {'id': None, 'name': None}
        collision_type = {'top': False, 'bottom': False, 'left': False, 'right': False}
        # X
        self.rect.x += movement[0]
        hit_list = self.__test_collide(tiles, entities)
        for tile in hit_list:
            if movement[0] > 0:
                self.rect.right = tile[0].left
                collision_type['right'] = True
            if movement[0] < 0:
                self.rect.left = tile[0].right
                collision_type['left'] = True
            tile_name['id'] = tile[2]
            tile_name['name'] = tile[1]
        # Y
        self.rect.y += movement[1]
        hit_list = self.__test_collide(tiles, entities)
        for tile in hit_list:
            if movement[1] > 0:
                if tile[1] != 'human':  # Это плохая штука!
                    self.rect.bottom = tile[0].top
                collision_type['bottom'] = True
            if movement[1] < 0:
                self.rect.top = tile[0].bottom
                collision_type['top'] = True
            tile_name['id'] = tile[2]
            tile_name['name'] = tile[1]

        return (tile_name, collision_type)


class Entity():
    def __init__(self, name, x, y, width, height, image=None, id=42):
        self.name = name
        self.id = id

        self.obj = physics(x, y, width, height)

        self.image = image
        self.frame = 0
        self.color = (0, 0, 0)

        self.alpha = None
        self.rotation = 0
        self.flip_x = False
        self.flip_y = False
        self.action = 'idle'

    def get_pos(self):
        return (self.obj.rect.x, self.obj.rect.y)

    def get_size(self):
        return (self.obj.rect.width, self.obj.rect.height)

    def get_rect(self):
        return self.obj.rect

    def set_pos(self, x, y):
        self.obj.rect.x = x
        self.obj.rect.y = y

    def set_size(self, width, height):
        self.obj.rect.width = width
        self.obj.rect.height = height

    # def move(self, movement, tiles):
    #    self.obj.move(movement, tiles)

    def collide_rect(self, rect):
        if self.obj.rect.colliderect(rect):
            return True

    def collide_point(self, point):
        if self.obj.rect.collidepoint(point):
            return True

    def flip(self, img):
        return pg.transform.flip(img, self.flip_x, self.flip_y)

    def render(self, display, camera=(0, 0)):
        image_to_render = None
        if self.image != None:
            image_to_render = self.image
            self.set_size(*image_to_render.get_size())

        if self.name in animation_higher_database and self.action in animation_higher_database[self.name]:
            self.frame += 1
            if self.frame > len(animation_higher_database[self.name][self.action]) - 1:
                self.frame = 0
            img_id = animation_higher_database[self.name][self.action][self.frame]
            image_to_render = animation_database[img_id]
            self.set_size(*image_to_render.get_size())

        if image_to_render != None:
            image_to_render = pg.transform.rotate(image_to_render, self.rotation)
            display.blit(self.flip(image_to_render), (self.get_pos()[0] - camera[0], self.get_pos()[1] - camera[1]))

        else:
            pg.draw.rect(display, self.color,
                         (self.get_pos()[0] - camera[0], self.get_pos()[1] - camera[1], *self.get_size()))
