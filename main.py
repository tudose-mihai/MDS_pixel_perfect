""" main loop """

# pylint: disable = 

import pygame as pg
import display as dp
import button as btn

##################ACTIVATE MAINMENU##################

BUTTONS = []
BUTTONS.append(btn.Button(710, 10, "MENU0", lambda: printmsg("MENU0")))
BUTTONS.append(btn.Button(805, 10, "Brush", lambda: activateBrush()))
BUTTONS.append(btn.Button(710, 60, "MENU2", lambda: printmsg("MENU2")))
BUTTONS.append(btn.Button(805, 60, "MENU3", lambda: printmsg("MENU3")))
LMC = lambda: printmsg("LEFT MOUSE CLICK")
RMC = lambda: printmsg("RIGHT MOUSE CLICK")

##################ACTIVATE BRUSH##################

def activateBrush():
    global BUTTONS, LMC, RMC
    BUTTONS.clear()
    BUTTONS.append(btn.Button(710, 10, "BRUSH0", lambda: printmsg("BRUSH0")))
    BUTTONS.append(btn.Button(805, 10, "BRUSH1", lambda: printmsg("BRUSH1")))
    BUTTONS.append(btn.Button(710, 60, "BRUSH2", lambda: printmsg("BRUSH2")))
    BUTTONS.append(btn.Button(805, 60, "RETURN", lambda: returnMain()))
    LMC = lambda: printmsg("LEFT BRUSH CLICK")
    RMC = lambda: printmsg("RIGHT BRUSH CLICK")

# TODO Brush functions

####################################

def returnMain():
    global BUTTONS, LMC, RMC
    BUTTONS.clear()
    BUTTONS.append(btn.Button(710, 10, "MENU0", lambda: printmsg("MENU0")))
    BUTTONS.append(btn.Button(805, 10, "Brush", lambda: activateBrush()))
    BUTTONS.append(btn.Button(710, 60, "MENU2", lambda: printmsg("MENU2")))
    BUTTONS.append(btn.Button(805, 60, "MENU3", lambda: printmsg("MENU3")))
    LMC = lambda: printmsg("LEFT MOUSE CLICK")
    RMC = lambda: printmsg("RIGHT MOUSE CLICK")

def printmsg(message):
    """docstring"""
    print(message)

##################MAINLOOP##################

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
