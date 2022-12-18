import pygame as pg

WIN_SIZE = (960, 600)
WIN_RES = (WIN_SIZE[0] // 3, WIN_SIZE[1] // 3)
J = WIN_SIZE[0] // WIN_RES[0]


screen = pg.display.set_mode(WIN_SIZE)
display = pg.Surface(WIN_RES)
camera = [0, 0]

FPS = 60
clock = pg.time.Clock()

keys = {'up': False, 'down': False, 'right': False, 'left': False, 'run': False}
can_input = True

animation_database = {}
animation_higher_database = {}

player_movement = [0, 0]
player_momentum = 2
air_timer = 0
speed = 1
stamina = 100

ds = WIN_RES[0]*3 // 320
ground = []
ground_chunks = {}

falling_blocks = []
falling_blocks_chunk = {}
momentum_fall = 0

back_ground_img = [pg.image.load('data/assets/sprites/background_1.png').convert_alpha(), pg.image.load('data/assets/sprites/background_2.png').convert_alpha()]
back_ground = {}
ground_img = pg.image.load('data/assets/sprites/ground_1.png').convert_alpha()