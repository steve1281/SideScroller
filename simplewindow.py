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
    def __init__(self, text="", x=50, y=50, width=500, height=232):
        super(Feedback, self).__init__(text)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def setText(self, raw_text):
        if not self.open_flag:
            self.image = pygame.Surface((0,0))
            self.rect = ((0,0),(0,0))
        else:
            texts = list(raw_text.split("\n"))
            box = pygame.Surface((self.width,self.height))
            box.fill(white)
            for i in range(len(texts)):
                text = self.font.render(texts[i], 1, (0, 0, 0))
                textpos = text.get_rect()
                textpos.centery = box.get_rect().centery + 30 * i
                textpos.centerx += 20
                box.blit(text, textpos)
            pygame.draw.rect(box,CMap.blue,(0, 0, self.width, self.height),2)
            pygame.draw.rect(box, CMap.red, (5, 5, 20, 20))
            self.image = box
            self.rect = ((self.x, self.y),(self.width, self.height))

    def evaluatePos(self, pos):
        x = pos[0] - self.x
        y = pos[1] - self.y
        if (x < 0 or y < 0 or
            x > self.width or
            y > self.height):
            return
        our_pos = (pos[0]-self.x ,pos[1] -self.y)
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

        window.fill(white)
        window.blit(test, (20, 50),rect)
        window.blit(test, (30, 50),rect2)
        window.blit(feedback.image,feedback.rect)

        feedback.setText("1. First option.\n2. Second option\n3. Third option.")
        clock.tick(fps)
        pygame.display.update()


    pygame.quit()


