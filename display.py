""" display module """

import pygame as pg

# WINDOW SIZE

WIDTH = 900
HEIGHT = 500
SCALE = 1
SIDEBAR_WIDTH = 200

# BASIC COLORS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (238, 130, 238)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
AQUA = (0, 255, 255)
DARK_GREEN = (0, 128, 0)

# PHOTOSHOP COLORS

PS0 = (221, 221, 221)
PS1 = (83, 83, 83)
PS2 = (66, 66, 66)
PS3 = (40, 40, 40)

# CREATE WINDOW

pg.init()
SCREEN = pg.Surface([WIDTH, HEIGHT])
pg.display.set_caption("image_editor")
# ICON = pg.image.load("")
# pg.display.set_icon(ICON)
WINDOW = pg.display.set_mode((int(WIDTH * SCALE), int(HEIGHT * SCALE)))

# LAYERS

BASE = pg.Surface([WIDTH-SIDEBAR_WIDTH, HEIGHT])
BASE.blit(pg.image.load("default.png"), (0, 0))

CHANGES = pg.Surface([WIDTH-SIDEBAR_WIDTH, HEIGHT], pg.SRCALPHA)
#TODO CHANGES LAYER
#TODO FILTER LAYER
