#!/usr/bin/env python

import pygame
from colors import CMap

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text):
        pygame.sprite.Sprite.__init__(self)
        self.open_flag = False
        self.font = pygame.font.Font(None, 36)
        self.setText(text)

    def setText(self, text):
        pass

class Feedback(TextSprite):

    def setText(self, text):
        if not self.open_flag:
            self.image = pygame.Surface((0,0))
            self.rect = ((0,0),(0,0))
        else:
            box = pygame.Surface((400,132))
            text = self.font.render(text, 1, (0, 0, 0))
            textpos = text.get_rect()
            textpos.centery = box.get_rect().centery
            textpos.centerx += 20
            box.fill(white)
            box.blit(text, textpos)
            pygame.draw.rect(box,CMap.blue,(0,0,400,132),2)
            pygame.draw.rect(box, CMap.red, (5, 5, 20, 20))
            self.image = box
            self.rect = ((44,50),(400,32))

    def evaluatePos(self, pos):
        x = pos[0] - 44
        y = pos[1] - 50
        if x < 0 or y < 0 or x > 400 or y > 132:
            return
        our_pos = (pos[0]-44 ,pos[1] -50)
        # self.setText("position is = %s" % str(our_pos))
        if our_pos[0] > 5 and our_pos[0] < 25 and our_pos[1] > 5 and our_pos[1] < 25:
            self.image = pygame.Surface((0,0))
            self.rect = ((0,0),(0,0))
            self.open_flag = False
            pygame.display.update()

    def openDialog(self):
        self.open_flag = True
        pygame.display.update()

if  __name__ == "__main__":
    pygame.init()
    size = width, height = 600, 620
    window = pygame.display.set_mode(size)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)

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
    feedback = Feedback("Hello Screen")

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

        window.fill(white)
        window.blit(test, (20, 50),rect)
        window.blit(test, (30, 50),rect2)
        window.blit(feedback.image,feedback.rect)

        feedback.setText("simple test")
        clock.tick(fps)
        pygame.display.update()


    pygame.quit()


