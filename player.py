#!/usr/bin/env python


import pygame
from colors import *

class Player(pygame.sprite.Sprite):
    def __init__(self, color=blue, width=32, height=48):
        self.width = width
        self.height = height
        super(Player, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill( color )
        self.set_properties()
        self.rect = self.image.get_rect()
        self.hspeed = 0
        self.vspeed = 0
        self.level = None

    def set_properties(self):
        self.rect = self.image.get_rect()
        self.origin_x = self.rect.centerx
        self.origin_y= self.rect.centery
        self.speed = 5

    def set_position(self, x, y):
        self.rect.x = x - self.origin_x
        self.rect.y = y - self.origin_y

    def set_level(self, level):
        self.level = level
        self.set_position(level.player_start_x, level.player_start_y)
        self.hspeed = 0
        self.vspeed = 0

    def update(self, collidable=pygame.sprite.Group(), event = None):
        self.experience_gravity()
        self.rect.x += self.hspeed

        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            if  self.hspeed > 0:
                self.rect.right = collided_object.rect.left
            elif  self.hspeed < 0:
                self.rect.left = collided_object.rect.right

        self.rect.y += self.vspeed
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            if  self.vspeed > 0:
                self.rect.bottom = collided_object.rect.top
                self.vspeed = 0
            elif  self.vspeed < 0:
                self.rect.top = collided_object.rect.bottom
                self.vspeed = 0

        if not event is None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.hspeed = -self.speed

                if event.key == pygame.K_RIGHT:
                    self.hspeed = self.speed

                if event.key == pygame.K_UP:
                    if self.vspeed == 0:
                        self.vspeed = -(self.speed)*2.5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if self.hspeed < 0:
                        self.hspeed == 0

                if event.key == pygame.K_RIGHT:
                    if self.hspeed > 0:
                        self.hspeed == 0

    def experience_gravity(self, gravity = .35):
        if self.vspeed == 0:
            self.vspeed = 1
        else:
            self.vspeed += gravity


