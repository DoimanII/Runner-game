import pygame as pg

WIN_SIZE = (800, 640)
WIN_RES = (WIN_SIZE[0] // 2, WIN_SIZE[1] // 2)

screen = pg.display.set_mode(WIN_SIZE)
display = pg.Surface(WIN_RES)
camera = [0, 0]

FPS = 60
clock = pg.time.Clock()

keys = {'up': False, 'down': False, 'right': False, 'left': False}
can_input = True


animation_database = {}
animation_higher_database = {}

player_movement = [0, 0]
player_momentum = 2
air_timer = 0
ground = []

falling_blocks = []
momentum_fall = 0
