"""docstring"""

# pylint: disable = invalid-name

import pygame as pg
from display import PS0, PS2, SCREEN

class Button:
    """docstring"""
    def __init__(self, x, y, text, function,
                 width=85, height=40, color=PS0, text_size=32, text_color=PS2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.function = function

        # BUTTON TEXT
        self.font = pg.font.Font('m5x7.ttf', text_size)
        self.text = self.font.render(text, False, text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.x + self.width // 2), (self.y + self.height // 2)

    def draw(self):
        """docstring"""
        pg.draw.rect(SCREEN, self.color, self.rect)
        SCREEN.blit(self.text, self.text_rect)
