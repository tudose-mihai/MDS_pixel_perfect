""" main loop """

# pylint: disable = 

import pygame as pg
import display as dp
import button as btn
import os, copy, time, math
##################ACTIVATE MAINMENU##################

BUTTONS = []
BUTTONS.append(btn.Button(710, 10, "Browser", lambda: activateBrowser()))
BUTTONS.append(btn.Button(805, 10, "Brush", lambda: activateBrush()))
BUTTONS.append(btn.Button(710, 60, "Polygons", lambda: activatePolygonBrush()))
BUTTONS.append(btn.Button(805, 60, "MENU3", lambda: printmsg("MENU3")))
LMC = lambda: printmsg("LEFT MOUSE CLICK")
RMC = lambda: printmsg("RIGHT MOUSE CLICK")
LMC_RELEASE = lambda: print('mainnn')

##################ACTIVATE BROWSER##################
page = 0
path = os.getcwd()
original_path = path
files = os.listdir(path)
def activateBrowser():
    global BUTTONS, LMC, RMC
    BUTTONS.clear()
    files = os.listdir(path)
    x, y = 710, 60
    minIndex, maxIndex = 14*page, 14*(page+1)
    for i in range(minIndex,min(len(files), maxIndex)):
        BUTTONS.append(btn.Button(x, y, files[i], lambda x = files[i]: browserAction(x)))
        if i % 2 == 0:
            x = 805
        else:
            x, y = 710, y + 50
    BUTTONS.append(btn.Button(710, 10, "PGUP", lambda: pageIncrement()))
    BUTTONS.append(btn.Button(805, 10, "PGDOWN", lambda: pageDecrement()))
    BUTTONS.append(btn.Button(710, 450, "BACK", lambda: browserUp()))
    BUTTONS.append(btn.Button(805, 450, "RETURN", lambda: returnMain()))
    LMC = lambda: printmsg("LEFT MOUSE CLICK")
    RMC = lambda: printmsg("RIGHT MOUSE CLICK")

def browserAction(name):
    global path
    imageExtensions = ['.png', '.jpg', '.jpeg', '.bmp']
    if '.' in name:  # not a file
        extension = name[name.rindex('.'):]
        if extension in imageExtensions: # is an image
            dp.BASE.blit(pg.image.load(name), (0, 0)) # load image
    else:  # is a file
        if path[-1] != '\\': # C: -> C:\
            path += '\\'
        path, page = path + name, 0
    activateBrowser()

def browserUp():
    global path, files
    path = path[:path.rindex("\\")]
    files = os.listdir(path)
    if path[-1] == ":":
        path += '\\'
    activateBrowser()

def pageIncrement():
    global page, files
    if (page+1)*16 <= len(files):
        page += 1
        activateBrowser()

def pageDecrement():
    global page
    if page > 0:
        page -= 1
        activateBrowser()

##################ACTIVATE POLYGON BRUSH##################
POLYGON_EDGE_SIZE = 6
POLYGON_EDGE_COLOR = dp.WHITE
POLYGON_SHAPE = "Square"
POLYGON_POS = None

def activatePolygonBrush():
    global BUTTONS, LMC, RMC, LMC_RELEASE

    BUTTONS.clear()
    BUTTONS.append(btn.Button(710, 10, "SIZE+", lambda: changePolygonEdgeSize(2)))
    BUTTONS.append(btn.Button(805, 10, "SIZE-", lambda: changePolygonEdgeSize(-2)))

    BUTTONS.append(btn.Button(710, 60, "", lambda: changePolygonEdgeColor(dp.WHITE), color=dp.WHITE))
    BUTTONS.append(btn.Button(805, 60, "", lambda: changePolygonEdgeColor(dp.BLACK), color=dp.BLACK))
    BUTTONS.append(btn.Button(710, 110, "", lambda: changePolygonEdgeColor(dp.RED), color=dp.RED))
    BUTTONS.append(btn.Button(805, 110, "", lambda: changePolygonEdgeColor(dp.GREEN), color=dp.GREEN))
    BUTTONS.append(btn.Button(710, 160, "", lambda: changePolygonEdgeColor(dp.BLUE), color=dp.BLUE))
    BUTTONS.append(btn.Button(805, 160, "", lambda: changePolygonEdgeColor(dp.VIOLET), color=dp.VIOLET))
    BUTTONS.append(btn.Button(710, 210, "", lambda: changePolygonEdgeColor(dp.YELLOW), color=dp.YELLOW))
    BUTTONS.append(btn.Button(805, 210, "", lambda: changePolygonEdgeColor(dp.ORANGE), color=dp.ORANGE))
    BUTTONS.append(btn.Button(710, 260, "", lambda: changePolygonEdgeColor(dp.AQUA), color=dp.AQUA))
    BUTTONS.append(btn.Button(805, 260, "", lambda: changePolygonEdgeColor(dp.DARK_GREEN), color=dp.DARK_GREEN))

    BUTTONS.append(btn.Button(710, 310, "Square", lambda: changePolygonShape("Square")))
    BUTTONS.append(btn.Button(805, 310, "Rectangle", lambda: changePolygonShape("Rectangle")))
    BUTTONS.append(btn.Button(710, 360, "Circle", lambda: changePolygonShape("Circle")))
    BUTTONS.append(btn.Button(805, 360, "Oval", lambda: changePolygonShape("Oval")))

    BUTTONS.append(btn.Button(710, 450, "CLEAR", lambda: clearChanges()))
    BUTTONS.append(btn.Button(805, 450, "RETURN", lambda: returnMain()))
    LMC_RELEASE = lambda: drawPolygon(POLYGON_EDGE_SIZE, POLYGON_EDGE_COLOR, POLYGON_SHAPE)
    LMC         = lambda: previewPolygon(POLYGON_EDGE_SIZE, POLYGON_EDGE_COLOR, POLYGON_SHAPE)
    RMC         = lambda: print("RMC polygon")

def changePolygonShape(x):
    global POLYGON_SHAPE
    POLYGON_SHAPE = x

def changePolygonEdgeColor(x):
    global POLYGON_EDGE_COLOR
    POLYGON_EDGE_COLOR = x

def changePolygonEdgeSize(x):
    global POLYGON_EDGE_SIZE
    if POLYGON_EDGE_SIZE == 2 and x < 0:
        POLYGON_EDGE_SIZE = 2
    else:
        POLYGON_EDGE_SIZE = POLYGON_EDGE_SIZE + x

def clearPolygonChanges():
    dp.PREVIEW = pg.Surface([dp.WIDTH-dp.SIDEBAR_WIDTH, dp.HEIGHT], pg.SRCALPHA)

def previewPolygon(size, color, shape):
    global POLYGON_CLICK, POLYGON_POS
    if POLYGON_POS is None:
        POLYGON_POS = (mouse_x, mouse_y)
    else:
        init_x, init_y = POLYGON_POS
        dp.PREVIEW = pg.Surface([dp.WIDTH-dp.SIDEBAR_WIDTH, dp.HEIGHT], pg.SRCALPHA)
        if shape == "Rectangle":
            pg.draw.rect(dp.PREVIEW, color, (init_x, init_y, mouse_x - init_x, mouse_y - init_y), size)
        elif shape == "Square":
            x_offset, y_offset = mouse_x - init_x, mouse_y - init_y
            x_offset, y_offset = min(x_offset, y_offset), min(x_offset, y_offset)
            pg.draw.rect(dp.PREVIEW, color, (init_x, init_y, x_offset, y_offset), size)
        elif shape == "Circle":
            pg.draw.circle(dp.PREVIEW, color, (init_x, init_y), math.dist((mouse_x,mouse_y),(init_x, init_y)), size)
        elif shape == "Oval":
            pg.draw.ellipse(dp.PREVIEW, color, (init_x, init_y, mouse_x - init_x, mouse_y - init_y), size)

def drawPolygon(size, color, shape):
    global POLYGON_CLICK, POLYGON_POS
    if POLYGON_POS is not None:
        init_x, init_y = POLYGON_POS
        if shape == "Rectangle":
            dp.PREVIEW = pg.Surface([dp.WIDTH-dp.SIDEBAR_WIDTH, dp.HEIGHT], pg.SRCALPHA)
            pg.draw.rect(dp.CHANGES, color, (init_x, init_y, mouse_x - init_x, mouse_y - init_y), size)
        elif shape == "Square":
            x_offset, y_offset = mouse_x - init_x, mouse_y - init_y
            x_offset, y_offset = min(x_offset, y_offset), min(x_offset, y_offset)
            dp.PREVIEW = pg.Surface([dp.WIDTH - dp.SIDEBAR_WIDTH, dp.HEIGHT], pg.SRCALPHA)
            pg.draw.rect(dp.CHANGES, color, (init_x, init_y, x_offset, y_offset), size)
        elif shape == "Circle":
            dp.PREVIEW = pg.Surface([dp.WIDTH - dp.SIDEBAR_WIDTH, dp.HEIGHT], pg.SRCALPHA)
            pg.draw.circle(dp.CHANGES, color, (init_x, init_y), math.dist((mouse_x,mouse_y),(init_x, init_y)), size)
        elif shape == "Oval":
            dp.PREVIEW = pg.Surface([dp.WIDTH-dp.SIDEBAR_WIDTH, dp.HEIGHT], pg.SRCALPHA)
            pg.draw.ellipse(dp.CHANGES, color, (init_x, init_y, mouse_x - init_x, mouse_y - init_y), size)
        POLYGON_POS = None

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
    BUTTONS.append(btn.Button(710, 310, "ERASER", lambda: changeColor(dp.ERASER)))
    BUTTONS.append(btn.Button(805, 310, "CLEAR", lambda: clearChanges()))
    BUTTONS.append(btn.Button(805, 450, "RETURN", lambda: returnMain()))
    LMC = lambda: drawBrush(BRUSH_SIZE, BRUSH_COLOR)
    RMC = lambda: drawBrush(BRUSH_SIZE + 8, dp.ERASER)

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
    BUTTONS.append(btn.Button(710, 10, "Browser", lambda: activateBrowser()))
    BUTTONS.append(btn.Button(805, 10, "Brush", lambda: activateBrush()))
    BUTTONS.append(btn.Button(710, 60, "Polygons", lambda: activatePolygonBrush()))
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
    dp.SCREEN.blit(dp.PREVIEW, (0, 0))

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
                LMC_RELEASE()
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
