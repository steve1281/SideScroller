#!/usr/bin/env python

import pygame
from colors import CMap

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=CMap.blue):
        self.width = width
        self.height = height
        super(Block, self).__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill( color )

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y



