""" main loop """

# pylint: disable = 

import pygame as pg
import display as dp
import menu0

# LOAD MAIN MENU SIDEBAR BUTTONS/ CANVAS MOUSE ACTIONS
BUTTONS = menu0.BUTTONS
LMC = menu0.LMC
RMC = menu0.RMC

# MAIN LOOP
RUN = True
while RUN:
    dp.SCREEN.fill(dp.BLACK)

    # DRAW SIDEBAR
    pg.draw.rect(dp.SCREEN, dp.PS1, (dp.WIDTH-dp.SIDEBAR_WIDTH, 0, dp.SIDEBAR_WIDTH, dp.HEIGHT))
    for button in BUTTONS:
        button.draw()

    # DRAW CANVAS
    dp.SCREEN.blit(dp.BASE, (0, 0))

    # UPDATE
    pg.transform.scale(dp.SCREEN, (int(dp.WIDTH * dp.SCALE), int(dp.HEIGHT * dp.SCALE)), dp.WINDOW)
    pg.display.update()

    # EVENT
    mouse_x, mouse_y = pg.mouse.get_pos()
    mouse_x, mouse_y = mouse_x // dp.SCALE, mouse_y // dp.SCALE

    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            # CLICK CANVAS
            if mouse_x < (dp.WIDTH-dp.SIDEBAR_WIDTH):
                if event.button == 1:
                    LMC()
                elif event.button == 3:
                    RMC()

            # CLICK SIDEBAR BUTTON
            else:
                for button in BUTTONS:
                    if button.rect.collidepoint(mouse_x, mouse_y):
                        button.function()

        if event.type == pg.QUIT:
            RUN = False

pg.quit()
