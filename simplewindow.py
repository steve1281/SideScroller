#!/usr/bin/env python

import pygame

if  __name__ == "__main__":
    pygame.init()
    size = width, height = 400, 320
    window = pygame.display.set_mode(size)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    window.fill(white)
    rect = pygame.Rect((20,50),(100,200))
    points_list = [ (20,50), (3, 120), (100, 90), (100, 120), ]

    pygame.draw.rect(window, red, rect, 3) 
    pygame.draw.polygon(window, red, points_list, 3) 
    pygame.draw.circle(window, red, (width/2, height/2), 100, 1) 
    pygame.draw.line(window, red, (20,20), (200,275), 5)

    pygame.display.update()
    running = True
    while running:
        for event in pygame.event.get():
	    if (event.type == pygame.QUIT or 
	        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
	        running = False
    pygame.quit()


