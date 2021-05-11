import math
import pygame
import sys
from copy import *
pygame.init()
pygame.font.init()
pygame.display.set_caption('Mihai Tudose - Hex')

myfont = pygame.font.SysFont('Arial', 20)
SIZE = (1000, 1000)
screen = pygame.display.set_mode(SIZE)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
WHITE = (255, 255, 255)
GREEN = (0,200,0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (50, 50, 255)
RED = (255, 0, 0)
THICKNESS = 3
BOARD_SIZE = 5
screen.fill(BLACK)
SIDE = 40
debug = 0
neighbours = [(-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1), (0, -1)]
turn = 1
method = 0
class Node:
    def __init__(self, row, column, player):
        self.row = row
        self.col = column
        self.player = player
class TreeNode:
    def __init__(self, value, succesors, board_state, blue_moves, red_moves):
        self.value = value
        self.succesors = succesors
        self.board_state = board_state
        self.blue_moves = blue_moves
        self.red_moves = red_moves
def define_sizes(hexagons, circles):
    sCos, sSin = SIDE * math.cos(math.radians(30)), SIDE * math.sin(math.radians(30))
    p1, p2, offset = 30, 200, 36
    for column in range(BOARD_SIZE):
        for row in range(BOARD_SIZE):
            p1 += 68
            hexagons[column][row] = [(p1, p2),
                                     (p1 + sCos, p2 - sSin),
                                     (p1 + 2 * sCos, p2),
                                     (p1 + 2 * sCos, p2 + SIDE),
                                     (p1 + sCos, p2 + SIDE + sSin),
                                     (p1, p2 + SIDE),
                                     (p1, p2)]
            circles[column][row] = (p1 + sCos, p2 + sSin)
        p2 += 60 + 1
        p1 = 30 + offset
        offset += 33
def hex_clicked(x1, y1):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x2, y2 = circles[i][j]
            if (x2 - x1) ** 2 + (y2 - y1) ** 2 < (SIDE * 0.9) ** 2:
                return i, j
    return -1, -1
def update_polygons():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if nodes[i][j].player == 1:
                pygame.draw.polygon(screen, LIGHT_BLUE, hexagons[i][j])
            elif nodes[i][j].player == -1:
                pygame.draw.polygon(screen, RED, hexagons[i][j])
            else:
                x, y = circles[i][j]
                if debug == 1:
                    textsurface = myfont.render(str(get_score_for(nodes, i, j, turn)), False, (0, 0, 0))
                    screen.blit(textsurface, (x - 15, y - 8))
                # textsurface = myfont.render(str(dist_blue[i][j])+","+str(dist_red[i][j]), False, (0, 0, 0))

            pygame.draw.polygon(screen, BLUE, hexagons[i][j], width=3)

            # pygame.draw.circle(screen, RED, circles[i][j], SIDE * 0.9, width=1)
def old_click_event(i, j):
    if (nodes[i][j].player == -1) or (nodes[i][j].player == 1):
        nodes[i][j].player = 0
    elif state == (1, 0, 0):
        nodes[i][j].player = 1
    else:
        nodes[i][j].player = -1
def new_click_event(i, j):
    if is_valid(i, j, turn) and nodes[i][j].player == 0:
        if turn == 1:
            nodes[i][j].player = 1
            if (i, j) in left_side:
                for k in neighbours:
                    x, y = k
                    if(0 <= i+x < BOARD_SIZE and 0 <= j+y < BOARD_SIZE and nodes[i+x][j+y].player == 0):
                        if (i+x, j+y) not in left_side:
                            left_side.append((i+x, j+y))
                        if (i, j) in left_side:
                            left_side.remove( (i, j) )
        else:
            nodes[i][j].player = -1
            if (i, j) in top_side:
                for k in neighbours:
                    x, y = k
                    if(0 <= i+x < BOARD_SIZE and 0 <= j+y < BOARD_SIZE and nodes[i+x][j+y].player == 0):
                        if (i + x, j + y) not in top_side:
                            top_side.append((i + x, j + y))
                        if (i, j) in top_side:
                            top_side.remove((i, j))

        return True
    return False
def is_valid(i, j, turn):
    tpl = (i, j)
    if(turn == 1 and tpl in left_side):
        return True
    elif(turn == -1 and tpl in top_side ):
        return True
    return False
def is_final():
    for i in range(BOARD_SIZE):
        if nodes[i][BOARD_SIZE-1].player == 1:
            return 1
        elif nodes[BOARD_SIZE-1][i].player == -1:
            return -1
    return 0
def reset_positions():
    left_side.clear()
    right_side.clear()
    top_side.clear()
    bottom_side.clear()
    for i in range(BOARD_SIZE):
        left_side.append((i, 0))
        right_side.append((i, BOARD_SIZE-1))
        top_side.append((0, i))
        bottom_side.append((BOARD_SIZE-1, i))
def update_distances_new(i, j, turn, board_state):
    list = [(i, j, 0)]
    path = []
    visited = [[False for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    visited[i][j] = True
    while len(list) > 0:
        coord = list.pop(0)
        x1, y1, distance = coord
        distance += 1
        foundNew = False
        for k in neighbours:
            x2, y2 = k
            if 0 <= x1+x2 < BOARD_SIZE and 0 <= y1+y2 < BOARD_SIZE:
                if board_state[x1 + x2][y1 + y2].player == 0 and not visited[x1 + x2][y1 + y2]:
                    foundNew = True
                    list.append((x1+x2,y1+y2, distance))
                    if turn == 1:
                        dist_blue[x1+x2][y1+y2] = min(dist_blue[x1+x2][y1+y2], distance)
                    elif turn == -1:
                        dist_red[x1+x2][y1+y2] = min(dist_red[x1+x2][y1+y2], distance)
                    visited[x1+x2][y1+y2] = True
        if not foundNew and not is_final_move(x1,y1,1):
            pass
        if not foundNew and is_final_move(x1,y1,turn):
            path.append((x1, y1, distance - 1)) #lista si pastram pe cel mai apropiat
    minDist = 100
    i, j = 0, 0
    for node in path:
        x, y, distance = node
        if distance < minDist:
            minDist = distance
            i = x
            j = y
    path = [(i, j, minDist)]
    visited = [[False for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    list = deepcopy(path)
    while len(list) > 0:
        coord = list.pop(0)
        x1, y1, distance = coord
        foundNew = False
        for k in neighbours:
            x2, y2 = k
            if 0 <= x1 + x2 < BOARD_SIZE and 0 <= y1 + y2 < BOARD_SIZE:
                if board_state[x1 + x2][y1 + y2].player == 0 and not visited[x1 + x2][y1 + y2]:
                    if (turn == 1 and dist_blue[x1+x2][y1+y2] == distance - 1) or (turn == -1 and dist_red[x1+x2][y1+y2] == distance - 1):
                        distance -= 1
                        list.append((x1 + x2, y1 + y2, distance))
                        path.append((x1 + x2, y1 + y2, distance))
                        visited[x1+x2][y1+y2] = True
                        break
    return path
def create_succesors(node, b_nodes, left_side, top_side, turn, depth):
    if depth > 0:
        moves = []
        added = []
        if turn == 1:
            moves = deepcopy(left_side)
            added = deepcopy(left_side)
        else:
            moves = deepcopy(top_side)
            added = deepcopy(top_side)
        for pair in moves:
            if turn == 1:
                moves = deepcopy(left_side)
            else:
                moves = deepcopy(top_side)
            i, j = pair
            board_state = deepcopy(b_nodes)
            found = False
            if is_valid(i, j, turn) and board_state[i][j].player == 0:
                board_state[i][j].player = turn
                if (i, j) in moves:
                    for k in neighbours:
                        x, y = k
                        if (0 <= i + x < BOARD_SIZE and 0 <= j + y < BOARD_SIZE and board_state[i + x][j + y].player == 0):
                            if (i+ x, j+ y) not in added:
                                moves.append( (i + x, j + y) )
                                moves.remove( (i, j))
                                added.append( (i + x, j + y) )
                                found = True
                                break
            if found:
                if turn == 1:
                    newNode = TreeNode(0,[], board_state, moves, deepcopy(top_side))
                else:
                    newNode = TreeNode(0,[], board_state, deepcopy(left_side), moves)
                node.succesors.append(newNode)

        for nextNode in node.succesors:
            create_succesors(nextNode, nextNode.board_state, nextNode.blue_moves, nextNode.red_moves, -turn, depth-1)
def is_final_move(x, y, turn):
    if nodes[x][y].player == 0:
        if turn == 1:
            if (x, y) in [ (i, BOARD_SIZE-1) for i in range(BOARD_SIZE)]:
                return True
        elif turn == -1:
            if (x, y) in [ (BOARD_SIZE-1, i) for i in range(BOARD_SIZE)]:
                return True
    return False
def get_score(board_state):
    turn = 1
    blue_list = []
    blue_score = -3
    red_score = 2
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board_state[x][y].player == turn:
                blue_list.append(update_distances_new(x, y, turn, board_state)) # returneaza drumuri posibile
    if len(blue_list) > 0:
        pathDistMin = 100
        pathNum = -1
        for i in range(len(blue_list)):
            path = blue_list[i]
            pathDist = path[0][2]
            if(pathDist<pathDistMin):
                pathNum = i
                pathDistMin = pathDist
        # print("Best blue path: ", blue_list[pathNum])
        # print("Score: ", blue_list[pathNum][0][2])
        blue_score = blue_list[pathNum][0][2]
    turn = -1
    red_list = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board_state[x][y].player == turn:
                red_list.append(update_distances_new(x, y, turn, board_state)) # returneaza drumuri posibile
    pathDistMin = 100
    pathNum = -1
    if len(red_list) > 0:
        for i in range(len(red_list)):
            path = red_list[i]
            pathDist = path[0][2]
            if (pathDist < pathDistMin):
                pathNum = i
                pathDistMin = pathDist
        # print("Best red path: ", red_list[pathNum])
        # print("Score: ", red_list[pathNum][0][2])
        red_score = red_list[pathNum][0][2]
    if method == 0:
        return blue_score - red_score
    else:
        return red_score
def get_score_for(nodes, x, y, turn):
    board_state = deepcopy(nodes)
    if(board_state[x][y].player == 0):
        (board_state[x][y]).player = turn
        return get_score(board_state)
def minmax(currNode, turn, depth, initDepth):
    if(turn == -1):
        maxValue = -100
        value = -1
        for succ in currNode.succesors:
            if len(succ.succesors) > 0:
                value = minmax(succ, -turn, depth - 1, initDepth)
            elif len(succ.succesors) == 0:
                x, y = get_move_made(currNode, succ)
                value = get_score_for(currNode.board_state, x, y, turn)
            maxValue = max(value, maxValue)
            succ.value = maxValue
        currNode.value = maxValue

    if(turn == 1):
        minValue = 100
        value = -1
        for succ in currNode.succesors:
            if len(succ.succesors) > 0:
                value = minmax(succ, -turn, depth - 1, initDepth)
            elif len(succ.succesors) == 0:
                x, y = get_move_made(currNode, succ)
                value = get_score_for(currNode.board_state, x, y, turn)
            minValue = min(value, minValue)
            succ.value = minValue
        currNode.value = minValue


    if depth == initDepth:
        otherNode = currNode
        for succ in currNode.succesors:
            if currNode.value == succ.value:
                otherNode = succ
                break
        x, y = get_move_made(currNode, otherNode)
        return get_move_made(currNode, otherNode)
    return currNode.value
def alphabeta(node, turn, depth, initDepth, alpha, beta):
    currNode = deepcopy(node)
    alphabetaCond = False
    if depth > 0:
        moves = []
        added = []
        if turn == 1:
            moves = deepcopy(node.blue_moves)
            added = deepcopy(node.blue_moves)
        else:
            moves = deepcopy(node.red_moves)
            added = deepcopy(node.red_moves)
        for pair in moves:
            if turn == 1:
                moves = deepcopy(node.blue_moves)
            else:
                moves = deepcopy(node.red_moves)
            i, j = pair
            board_state = deepcopy(currNode.board_state)
            maxValue = -100
            minValue = 100
            if is_valid(i, j, turn) and board_state[i][j].player == 0:
                board_state[i][j].player = turn
                if (i, j) in moves:
                    for k in neighbours:
                        x, y = k
                        if (0 <= i + x < BOARD_SIZE and 0 <= j + y < BOARD_SIZE and board_state[i + x][j + y].player == 0):
                            if (i+ x, j+ y) not in added and not alphabetaCond:
                                moves.append((i + x, j + y))
                                if (i, j) in moves:
                                    moves.remove((i, j))
                                added.append((i + x, j + y))
                                if turn == 1:
                                    newNode = TreeNode(0, [], board_state, moves, deepcopy(top_side))
                                else:
                                    newNode = TreeNode(0, [], board_state, deepcopy(left_side), moves)
                                currNode.succesors.append(newNode)
                                value = alphabeta(newNode, -turn, depth - 1, initDepth, alpha * turn, beta * (-turn))
                                newNode.value = value
                                if turn == 1:
                                    minValue = min(value, minValue)
                                    alpha = min(value, alpha)
                                    if alpha < beta:
                                        alphabetaCond = True
                                else:
                                    maxValue = max(value, maxValue)
                                    beta = max(value, beta)
                                    if beta< alpha:
                                        alphabetaCond = True

                    if turn == 1:
                        currNode.value = minValue
                    else:
                        currNode.value = maxValue
        if(depth < initDepth):
            return currNode.value
    elif depth == 0:
        value = get_score(currNode.board_state)
        return value
    if depth == initDepth:
        otherNode = currNode
        for succ in currNode.succesors:
            if currNode.value == succ.value:
                otherNode = succ
                break
        x, y = get_move_made(currNode, otherNode)
        return get_move_made(currNode, otherNode)
def get_move_made(node, otherNode):
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if (node.board_state[x][y].player != otherNode.board_state[x][y].player):
                return x, y
    return -1, -1

#initializare
left_side = []
right_side = []
top_side = []
bottom_side = []
turn = 1
hexagons = [[[] for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
circles = [[[] for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
nodes = [[Node(i, j, 0) for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
dist_blue = [[10 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
dist_red = deepcopy(dist_blue)
virtual_dist_blue = deepcopy(dist_blue)
virtual_dist_red = deepcopy(dist_blue)
define_sizes(hexagons, circles), screen.fill(GRAY), update_polygons(), reset_positions()
depth = 2
final = 0
alg = 0
player = 2
start = 0

#meniu introductiv
while True and start == 0:
    screen.fill(GRAY)
    realFonty = pygame.font.SysFont('Arial', 30)
    SELECTED = (220,220,220)
    UNSELECTED = (140, 140, 140)

    #3 butoane dificultate
    if depth == 2:
        pygame.draw.rect(screen, SELECTED, (100, 100, 200, 100))
    else:
        pygame.draw.rect(screen, UNSELECTED, (100, 100, 200, 100))
    textsurface = realFonty.render("easy", False, (0, 0, 0))
    screen.blit(textsurface, (120, 140))
    if depth == 4:
        pygame.draw.rect(screen, SELECTED, (400, 100, 200, 100))
    else:
        pygame.draw.rect(screen, UNSELECTED, (400, 100, 200, 100))
    textsurface = realFonty.render("medium", False, (0, 0, 0))
    screen.blit(textsurface, (420, 140))
    if depth == 6:
        pygame.draw.rect(screen, SELECTED, (700, 100, 200, 100))
    else:
        pygame.draw.rect(screen, UNSELECTED, (700, 100, 200, 100))
    textsurface = realFonty.render("hard", False, (0, 0, 0))
    screen.blit(textsurface, (720, 140))


    #2 butoane alegere algoritm
    if alg == 0:
        pygame.draw.rect(screen, SELECTED, (250, 300, 200, 100))
        pygame.draw.rect(screen, UNSELECTED, (570, 300, 200, 100))
    else:
        pygame.draw.rect(screen, UNSELECTED, (250, 300, 200, 100))
        pygame.draw.rect(screen, SELECTED, (570, 300, 200, 100))
    textsurface = realFonty.render("minmax", False, (0, 0, 0))
    screen.blit(textsurface, (270, 340))
    textsurface = realFonty.render("alphabeta", False, (0, 0, 0))
    screen.blit(textsurface, (590, 340))

    #3 butoane alegere nr jucatori , pc vs pc nu e inca implementat
    if player == 2:
        pygame.draw.rect(screen, SELECTED, (100, 500, 200, 100))
    else:
        pygame.draw.rect(screen, UNSELECTED, (100, 500, 200, 100))

    textsurface = realFonty.render("2 jucatori", False, (0, 0, 0))
    screen.blit(textsurface, (120, 540))

    if player == 1:
        pygame.draw.rect(screen, SELECTED, (400, 500, 200, 100))
    else:
        pygame.draw.rect(screen, UNSELECTED, (400, 500, 200, 100))
    textsurface = realFonty.render("1 jucator", False, (0, 0, 0))
    screen.blit(textsurface, (420, 540))

    if player == 0: # nu merge ..
        pygame.draw.rect(screen, SELECTED, (700, 500, 200, 100))
    else:
        pygame.draw.rect(screen, UNSELECTED, (700, 500, 200, 100))

    textsurface = realFonty.render("pc vs pc", False, (0, 0, 0))
    screen.blit(textsurface, (720, 540))

    pygame.draw.rect(screen, LIGHT_BLUE, (220, 800, 200, 100))
    textsurface = realFonty.render("Start!", False, (0, 0, 0))
    screen.blit(textsurface, (240, 840))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(),
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN :
            screen.fill(GRAY)
            x, y = pygame.mouse.get_pos()
            #interactivitate butoane
            state = pygame.mouse.get_pressed(num_buttons=3)
            if 100 <= x <= 300 and 100 <= y <= 200:
                depth = 2
            if 400 <= x <= 600 and 100 <= y <= 200:
                depth = 4
            if 700 <= x <= 900 and 100 <= y <= 200:
                depth = 6
            if 250 <= x <= 450 and 300 <= y <= 400:
                alg = 0
            if 570 <= x <= 770 and 300 <= y <= 400:
                alg = 1
            if 100 <= x <= 300 and 500 <= y <= 600:
                player = 2
            if 400 <= x <= 600 and 500 <= y <= 600:
                player = 1
            if 700 <= x <= 900 and 500 <= y <= 600:
                player = 0
            if 220 <= x <= 420 and 800 <= y <= 900:
                start = 1
            print(x, y)
        break

#interfata joc
while True:
    update_polygons()
    pygame.display.update()
    pygame.draw.rect(screen, GREEN, (880, 20, 100, 50))
    #afiseaza pentru fiecare pozitie care ar fi scorul tablei rezultante
    textsurface = myfont.render("debug", False, (0, 0, 0))
    screen.blit(textsurface, (900, 34))
    if turn == 1:
        turnMsg = "Randul lui Albastru"
        VERY_LIGHT_BLUE = (90,90,255)
        pygame.draw.rect(screen, VERY_LIGHT_BLUE, (30, 10, 190, 40))
        textsurface = myfont.render(turnMsg, False, (0, 0, 0))
    elif turn == -1:
        pygame.draw.rect(screen, RED, (30, 10, 190, 40))
        turnMsg = "Randul lui Rosu"
        textsurface = myfont.render(turnMsg, False, (0, 0, 0))
    screen.blit(textsurface, (40, 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(),
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN : #miscare jucator initiata de click
            screen.fill(GRAY)
            x, y = pygame.mouse.get_pos()
            state = pygame.mouse.get_pressed(num_buttons=3)
            i, j = hex_clicked(x, y)
            if (i, j) != (-1, -1)  and final == 0:
                print("clicked on", i, j)
                valid = new_click_event(i, j)
                if valid:
                    turn = -turn
            elif 880 <= x <= 980 and 20 <= y <= 70:
                debug = debug^1
            print("scor tabla: ", get_score(nodes))
            update_polygons()
            final = is_final()
            if (player == 1 and turn == -1): #miscare pc initiata de finalul miscarii jucatorului; face pe cat de repede posibil
                node = TreeNode(0, [], deepcopy(nodes), deepcopy(left_side), deepcopy(top_side))
                initDepth = deepcopy(depth)
                if alg == 0:
                    create_succesors(node, nodes, left_side, top_side, turn, depth)
                    i, j = minmax(node, turn, depth, initDepth)
                elif alg == 1:
                    node = TreeNode(0, [], deepcopy(nodes), deepcopy(left_side), deepcopy(top_side))
                    i, j = alphabeta(node, turn, depth, initDepth, 200 * turn, 200 * (-turn))
                valid = new_click_event(i, j)
                if valid:
                    turn = -turn
            update_polygons()


        #afisare ecran in caz de victorie (remiza este imposibila)
        if final == 1: #victorie albastru
            tinySide = 50
            realFonty = pygame.font.SysFont('Arial', 30)
            sCos, sSin = tinySide * math.cos(math.radians(30)), tinySide * math.sin(math.radians(30))
            p1, p2 = 700, 200
            hex_coords = [(p1, p2), (p1 + sCos, p2 - sSin), (p1 + 2 * sCos, p2), (p1 + 2 * sCos, p2 + tinySide),
                          (p1 + sCos, p2 + tinySide + sSin), (p1, p2 + tinySide), (p1, p2)]
            pygame.draw.polygon(screen, VERY_LIGHT_BLUE, hex_coords)
            turnMsg = "wins !"
            textsurface = realFonty.render(turnMsg, False, (0, 0, 0))
            screen.blit(textsurface, (800, 205))
        elif final == -1: #victorie rosu
                tinySide = 50
                realFonty = pygame.font.SysFont('Arial', 30)
                sCos, sSin = tinySide * math.cos(math.radians(30)), tinySide * math.sin(math.radians(30))
                p1, p2 = 700, 200
                hex_coords = [(p1, p2), (p1 + sCos, p2 - sSin), (p1 + 2 * sCos, p2), (p1 + 2 * sCos, p2 + tinySide),
                              (p1 + sCos, p2 + tinySide + sSin), (p1, p2 + tinySide), (p1, p2)]
                pygame.draw.polygon(screen, RED, hex_coords)
                turnMsg = "wins !"
                textsurface = realFonty.render(turnMsg, False, (0, 0, 0))
                screen.blit(textsurface, (800, 205))

        break

#interfata final joc
while True:
    pygame.display.update()

