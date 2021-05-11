#!/usr/bin/env python
import os, pygame, time
from pygame.compat import xrange_

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

SIZE = 255

def show(image):
    screen = pygame.display.get_surface()
    screen.fill((SIZE, SIZE, SIZE))
    screen.blit(image, (0, 0))
    pygame.display.flip()
    # while 1:
    #     event = pygame.event.wait()
    #     if event.type == pygame.QUIT:
    #         raise SystemExit
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         break


def main():
    pygame.init()

    pygame.display.set_mode((SIZE, SIZE))
    surface = pygame.Surface((SIZE, SIZE))

    pygame.display.flip()

    # Create the PixelArray.
    r, g, b = 0, 0, 0
    # Do some easy gradient effect.
    for k in range(4,SIZE,10):
        arr = pygame.PixelArray(surface)

        for i in range(SIZE):
            for j in range(SIZE):
                r = (i*255/SIZE)%k
                g = (j*255/SIZE)%k
                b = (i*(255-k)+j*k)%k
                arr[i, j] = (r, g, b)
        del arr
        print("running", k)
        show(surface)
    clicking = True
    while(1):
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicking = True
            screen = pygame.display.get_surface()
            pos = pygame.mouse.get_pos()
            state = pygame.mouse.get_pressed()
            x, y = pos
            arr = pygame.PixelArray(surface)
            brushSize = 3
            black = (0, 0, 0)
            offset = 0
            for i in range(-brushSize, 1):
                for j in range(2 * brushSize + 1 - 2 * abs(i)):
                    arr[x + i, y + j - offset] = (0, 0, 0)
                offset += 1
            for i in range(brushSize + 1):
                offset -= 1
                for j in range(2 * brushSize + 1 - 2 * abs(i)):
                    arr[x + i, y + j - offset] = (0, 0, 0)
            del arr
            show(surface)
        if event.type == pygame.MOUSEBUTTONUP:
            clicking = False
        if clicking == True and event.type == pygame.MOUSEMOTION:
            screen = pygame.display.get_surface()
            pos = pygame.mouse.get_pos()
            state = pygame.mouse.get_pressed()
            x, y = pos
            arr = pygame.PixelArray(surface)
            brushSize = 3
            black = (0,0,0)
            offset = 0
            for i in range(-brushSize, 1):
                for j in range(2 * brushSize + 1 - 2 * abs(i)):
                    arr[x+i, y+j - offset] = (0,0,0)
                offset += 1
            for i in range(brushSize + 1):
                offset -= 1
                for j in range(2 * brushSize + 1 - 2 * abs(i)):
                    arr[x+i, y+j - offset] = (0, 0, 0)
            del arr
            show(surface)

if __name__ == '__main__':
    main()