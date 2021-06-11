import os
import button
import copy

path = os.getcwd()
files = os.listdir(path)

imageExtensions = ['.png', '.jpg', '.jpeg', '.bmp']
imageName = ''
file_name = ''
done = False
active = False
page = 0

files = os.listdir(path)
yoffset = 50

BUTTONS = []


def browserUpdate():
    global BUTTONS
    BUTTONS.clear()
    files = os.listdir(path)
    x, y = 710, 60
    BUTTONS.append(button.Button(710, 10, "back", lambda: browserExit()))
    BUTTONS.append(button.Button(805, 10, "up", lambda: browserUp()))
    minIndex, maxIndex = 16*page, 16*(page+1)
    for i in range(minIndex,min(len(files), maxIndex)):
        name = copy.deepcopy(files[i])
        newButton = button.Button(x, y, files[i], lambda x = name: browserAction(x))
        BUTTONS.append(newButton)
        del newButton
        if i % 2 == 0:
            x = 805
        else:
            x = 710
            y += 50
    BUTTONS.append(button.Button(710, 460, "pgup", lambda: pageIncrement()))
    BUTTONS.append(button.Button(805, 460, "pgdown", lambda: pageDecrement()))


browserUpdate()  # initialization


def browserAction(name):
    global path
    print("clicked on ", name)
    if '.' in name:  # not a file
        extension = name[name.rindex('.'):]
        if extension in imageExtensions:
            imagePath = path + '\\' + name
            # image = pygame.image.load(path + '\\' + files[x])
            # ar modifica in display, dar nu stiu cum e preferabil in contextul asta
            imageName = name
    else:  # is a file
        if path[-1] != '\\':
            path += '\\'
        path += name
        page = 0
    browserUpdate()


def browserUp():
    global path, files
    path = path[:path.rindex("\\")]
    files = os.listdir(path)
    if path[-1] == ":":
        path += '\\'
    browserUpdate()


def browserExit():
    return 0


def pageIncrement():
    global page, files
    if (page+1)*16 <= len(files):
        page += 1
        browserUpdate()


def pageDecrement():
    global page
    if page > 0:
        page -= 1
        browserUpdate()
