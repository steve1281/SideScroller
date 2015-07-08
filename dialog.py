import pygame
from colors import CMap


class Feedback(pygame.sprite.Sprite):
    def __init__(self, text="", x=50, y=50, w=500, h=232):
        pygame.sprite.Sprite.__init__(self)
        self.open_flag = False
        self.font = pygame.font.Font(None, 36)
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.texts = []
        self.setText(text)

    def drawText(self):
        if not self.open_flag:
            self.image = pygame.Surface((0,0))
            self.rect = ((0,0),(0,0))
        else:
            box = pygame.Surface((self.width,self.height))
            box.fill(CMap.white)
            for i in range(len(self.texts)):
                text = self.font.render(self.texts[i], 1, (0, 0, 0))
                textpos = text.get_rect()
                textpos.centery = box.get_rect().centery + 30 * i
                textpos.centerx += 20
                box.blit(text, textpos)
            pygame.draw.rect(box,CMap.blue,(0, 0, self.width, self.height),2)
            pygame.draw.rect(box, CMap.red, (5, 5, 20, 20))
            self.image = box
            self.rect = ((self.x, self.y),(self.width, self.height))

    def setText(self, raw_text):
       texts = list(raw_text.split("\n"))
       self.drawText()

    def evaluatePos(self, pos):
        x = pos[0] - self.x
        y = pos[1] - self.y
        if (x < 0 or y < 0 or
            x > self.width or
            y > self.height):
            return
        our_pos = (pos[0]-self.x , pos[1] -self.y)
        if (our_pos[0] > 5 and
            our_pos[0] < 25 and
            our_pos[1] > 5 and
            our_pos[1] < 25):
            self.image = pygame.Surface((0,0))
            self.rect = ((0,0),(0,0))
            self.open_flag = False
            self.drawText()

    def openDialog(self):
        self.open_flag = True
        self.drawText()


