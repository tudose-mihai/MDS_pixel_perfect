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
BRUSH_SIZE = 6
BRUSH_COLOR = dp.WHITE

def activateBrush():
    global BUTTONS, LMC, RMC

    BUTTONS.clear()
    BUTTONS.append(btn.Button(710, 10, "SIZE+", lambda: changeSize(2)))
    BUTTONS.append(btn.Button(805, 10, "SIZE-", lambda: changeSize(-2)))
    BUTTONS.append(btn.Button(710, 60, "", lambda: changeColor(dp.WHITE), color= dp.WHITE))
    BUTTONS.append(btn.Button(805, 60, "", lambda: changeColor(dp.BLACK), color=dp.BLACK))
    BUTTONS.append(btn.Button(710, 110, "", lambda: changeColor(dp.RED), color=dp.RED))
    BUTTONS.append(btn.Button(805, 110, "", lambda: changeColor(dp.GREEN), color=dp.GREEN))
    BUTTONS.append(btn.Button(710, 160, "", lambda: changeColor(dp.BLUE), color=dp.BLUE))
    BUTTONS.append(btn.Button(805, 160, "", lambda: changeColor(dp.VIOLET), color=dp.VIOLET))
    BUTTONS.append(btn.Button(710, 210, "", lambda: changeColor(dp.YELLOW), color=dp.YELLOW))
    BUTTONS.append(btn.Button(805, 210, "", lambda: changeColor(dp.ORANGE), color=dp.ORANGE))
    BUTTONS.append(btn.Button(710, 260, "", lambda: changeColor(dp.AQUA), color=dp.AQUA))
    BUTTONS.append(btn.Button(805, 260, "", lambda: changeColor(dp.DARK_GREEN), color=dp.DARK_GREEN))
    BUTTONS.append(btn.Button(710, 310, "CLEAR", lambda: clearChanges()))
    BUTTONS.append(btn.Button(805, 450, "RETURN", lambda: returnMain()))
    LMC = lambda: drawBrush(BRUSH_SIZE, BRUSH_COLOR)
    RMC = lambda: printmsg("RIGHT BRUSH CLICK")

def changeColor(x):
    global BRUSH_COLOR
    BRUSH_COLOR = x

def changeSize(x):
    global BRUSH_SIZE
    if BRUSH_SIZE == 2 and x < 0:
        BRUSH_SIZE = 2
    else:
        BRUSH_SIZE = BRUSH_SIZE + x

def clearChanges():
    dp.CHANGES = pg.Surface([dp.WIDTH-dp.SIDEBAR_WIDTH, dp.HEIGHT], pg.SRCALPHA)

def drawBrush(size, color):
    pg.draw.circle(dp.CHANGES, color, (mouse_x, mouse_y), size)


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
LMC_IS_PRESSED = False
RMC_IS_PRESSED = False
while RUN:
    dp.SCREEN.fill(dp.BLACK)

    # DRAW SIDEBAR
    pg.draw.rect(dp.SCREEN, dp.PS1, (dp.WIDTH - dp.SIDEBAR_WIDTH, 0, dp.SIDEBAR_WIDTH, dp.HEIGHT))
    for button in BUTTONS:
        button.draw()

    # DRAW CANVAS
    dp.SCREEN.blit(dp.BASE, (0, 0))
    dp.SCREEN.blit(dp.CHANGES, (0, 0))

    # UPDATE
    pg.transform.scale(dp.SCREEN, (int(dp.WIDTH * dp.SCALE), int(dp.HEIGHT * dp.SCALE)), dp.WINDOW)
    pg.display.update()

    # EVENT
    mouse_x, mouse_y = pg.mouse.get_pos()
    mouse_x, mouse_y = mouse_x // dp.SCALE, mouse_y // dp.SCALE

    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                LMC_IS_PRESSED = True
            elif event.button == 3:
                RMC_IS_PRESSED = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                LMC_IS_PRESSED = False
            elif event.button == 3:
                RMC_IS_PRESSED = False

        if mouse_x < (dp.WIDTH - dp.SIDEBAR_WIDTH):
            # CLICK CANVAS
            if LMC_IS_PRESSED:
                LMC()

            if RMC_IS_PRESSED:
                RMC()

        # CLICK SIDEBAR BUTTON
        elif event.type == pg.MOUSEBUTTONDOWN:
            for button in BUTTONS:
                if button.rect.collidepoint(mouse_x, mouse_y):
                    button.function()

    if event.type == pg.QUIT:
        RUN = False

pg.quit()
