""" main menu sidebar buttons/ canvas mouse actions """

import button

# SIDEBAR BUTTONS

BUTTONS = []
BUTTONS.append(button.Button(710, 10, "TEST0", lambda: printmsg("TEST0")))
BUTTONS.append(button.Button(805, 10, "TEST1", lambda: printmsg("TEST1")))
BUTTONS.append(button.Button(710, 60, "TEST2", lambda: printmsg("TEST2")))
BUTTONS.append(button.Button(805, 60, "TEST3", lambda: printmsg("TEST3")))
BUTTONS.append(button.Button(710, 110, "TEST4", lambda: printmsg("TEST4")))
BUTTONS.append(button.Button(805, 110, "TEST5", lambda: printmsg("TEST5")))
BUTTONS.append(button.Button(710, 160, "TEST6", lambda: printmsg("TEST6")))
BUTTONS.append(button.Button(805, 160, "TEST7", lambda: printmsg("TEST7")))

# CANVAS MOUSE ACTIONS

LMC = lambda: printmsg("LEFT MOUSE CLICK")
RMC = lambda: printmsg("RIGHT MOUSE CLICK")

# FUNCTIONS

def printmsg(message):
    """docstring"""
    print(message)
