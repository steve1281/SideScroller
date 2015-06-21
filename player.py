#!/usr/bin/env python


import pygame
from colors import CMap
from imagefactory import ImageFactory

class Player(pygame.sprite.Sprite):
    def __init__(self, color=CMap.blue, width=32, height=48):
        self.images = ImageFactory()
        self.width = width
        self.height = height
        super(Player, self).__init__()

        self.direction = ""
        self.hspeed = 0
        self.vspeed = 0
        self.level = None

        self.set_custome()
        self.set_properties()
        self.rect = self.image.get_rect()

    def set_custome(self):
        # determine current direction
        direction = "standing"
        if self.vspeed < 0:
            direction = "up"
        elif self.vspeed > 0:
            direction = "down"
        elif self.vspeed == 0:
            if self.hspeed > 0:
                direction = "right"
            elif self.hspeed < 0:
                direction = "left"
            else:
                direction = "standing"
        if self.direction == direction:
            pass
        else:
            self.direction = direction
            self.image = self.images.getImage(direction)

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
    
    def did_collide(self, collidable=pygame.sprite.Group(), event = None):
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        return collision_list

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
        self.set_custome()

    def experience_gravity(self, gravity = .35):
        if self.vspeed == 0:
            self.vspeed = 1
        else:
            self.vspeed += gravity


