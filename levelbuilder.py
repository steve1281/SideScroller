#!/usr/bin/env python
import math
import pygame
from colors import *

if  __name__ == "__main__":
    pygame.init()
    size = width, height = 1200, 1000
    window = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    window.fill(white)

    pygame.display.update()
    to_draw = []
    draw_start_box = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif (event.type == pygame.MOUSEMOTION):
                mouse_pos = mouse_x, mouse_y = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    print pygame.mouse.get_pos()
                    event = None
                else:
                    rpos = mouse_pos
                    sx = math.floor(rpos[0]/10)*10
                    sy = math.floor(rpos[1]/10)*10
                    pos = (sx,sy)
                    draw_start_box = True
            elif event.type == pygame.MOUSEBUTTONUP:
	        if event.button == 3:
		    event = None
		else:
                    rpos = mouse_pos
                    sx = math.floor(rpos[0]/10)*10
                    sy = math.floor(rpos[1]/10)*10
                    final_pos = (sx,sy)

                    #final_pos = mouse_pos
                    draw_start_box = False
                    r = pygame.Rect(pos, (final_pos[0]-pos[0], final_pos[1]-pos[1]))
                    r.normalize()
                    to_draw += [r]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    target = open("level.dat",'w')
                    for platform in to_draw:
                        target.write("["+str(platform).split("(")[1].split(")")[0]+", black],\n")
                    target.close()
                    print "level written to level.dat"

                if event.key == pygame.K_BACKSPACE:
                    if len(to_draw):
                        to_draw.pop()

        window.fill(white)
        if (draw_start_box):
            pygame.draw.rect(window, red, pygame.Rect(pos, (mouse_pos[0]-pos[0], mouse_pos[1]-pos[1])))

        for item in to_draw:
            pygame.draw.rect(window, black, item)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


