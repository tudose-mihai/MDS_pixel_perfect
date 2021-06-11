""" main menu sidebar buttons/ canvas mouse actions """

import button

# SIDEBAR BUTTONS

BUTTONS_BRUSH = []
BUTTONS_BRUSH.append(button.Button(710, 10, "Size+", lambda: printmsg("Size+")))
BUTTONS_BRUSH.append(button.Button(805, 10, "Size-", lambda: printmsg("Size-")))
BUTTONS_BRUSH.append(button.Button(710, 60, "TEST2", lambda: printmsg("TEST2")))
BUTTONS_BRUSH.append(button.Button(805, 60, "Return", lambda: printmsg("return")))


# CANVAS MOUSE ACTIONS

LMC_BRUSH = lambda: printmsg("LEFT MOUSE CLICK")
RMC_BRUSH = lambda: printmsg("RIGHT MOUSE CLICK")

# FUNCTIONS

def printmsg(message):
    """docstring"""
    print(message)


def toggleBrowser(value):
    return value

    #BRUSH CONTROLLER

