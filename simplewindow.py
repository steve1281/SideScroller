#!/usr/bin/env python

import pygame
from colors import CMap
from dialog import Feedback

if  __name__ == "__main__":
    pygame.init()
    size = width, height = 600, 620
    window = pygame.display.set_mode(size)

    rect = pygame.Rect((20,50),(100,200))
    rect2 = pygame.Rect((20,50),(200,100))
    points_list = [ (20,50), (3, 120), (100, 90), (100, 120), ]

    test = pygame.Surface((800,600))
    img = pygame.image.load('brickwall.png').convert()
    for y in range(0,600,32):
        for x in range(0,800,32):
            test.blit( img,(x,y))

    clock = pygame.time.Clock()
    fps = 30
    feedback = Feedback("Hello Screen\nTest",10,50,300,200)

    pygame.display.update()
    running = True
    while running:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                feedback.evaluatePos(pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                feedback.openDialog()

        window.fill(CMap.white)
        window.blit(test, (20, 50),rect)
        window.blit(test, (30, 50),rect2)
        window.blit(feedback.image,feedback.rect)

        feedback.setText("1. First option.\n2. Second option\n3. Third option.")
        clock.tick(fps)
        pygame.display.update()


    pygame.quit()


