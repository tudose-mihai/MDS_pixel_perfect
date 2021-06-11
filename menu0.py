""" main menu sidebar buttons/ canvas mouse actions """

import button
from menu_brush import BUTTONS_BRUSH, LMC_BRUSH, RMC_BRUSH
from main import BUTTONS


# SIDEBAR BUTTONS

BUTTONS_MAIN = []
BUTTONS_MAIN.append(button.Button(710, 10, "Browse", lambda: toggleBrowser(1)))
BUTTONS_MAIN.append(button.Button(805, 10, "Brush", lambda: activateBrush()))
BUTTONS_MAIN.append(button.Button(710, 60, "TEST2", lambda: printmsg("TEST2")))
BUTTONS_MAIN.append(button.Button(805, 60, "TEST3", lambda: printmsg("TEST3")))

# CANVAS MOUSE ACTIONS

LMC_MAIN = lambda: printmsg("LEFT MOUSE CLICK")
RMC_MAIN = lambda: printmsg("RIGHT MOUSE CLICK")

# FUNCTIONS

def printmsg(message):
    """docstring"""
    print(message)


def toggleBrowser(value):
    return value


def activateBrush():
    BUTTONS_MAIN = BUTTONS_BRUSH
    print("brush activated")