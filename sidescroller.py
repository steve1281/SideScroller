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

    """
    def set_image(self, filename = None):
        if filename != None:
            self.image = pygame.image.load(filename).convert()
            self.image = pygame.transform.scale(self.image,(self.width,self.height))
            self.set_properties()
    """

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

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=blue):
        self.width = width
        self.height = height
        super(Block, self).__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill( color )

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

class Level(object):
    def __init__(self, player_object):
        self.object_list = pygame.sprite.Group()
        self.player_object = player_object
        self.player_start = self.player_start_x, self.player_start_y = 0, 0

    def update(self):
        self.object_list.update()

    def draw(self, window):
        window.fill(white)
        self.object_list.draw(window)

class Level_01( Level):
    def __init__(self,player_object):
        super(Level_01, self).__init__(player_object)
        self.player_start = self.player_start_x, self.player_start_y = 30, 10

        level = [
                # [x, y, width, height, color ]
                [2,134,365,47,black],
                [200,334,365,47,black],
                #[0,0,window_width,2,black],
                [0,window_height,window_width,2,black],
                [0,0,2,window_height,2,black],
                [window_width,0,2,window_height,2,black],
        ]
        for block in level:
            block = Block( block[0], block[1], block[2], block[3], block[4])
            self.object_list.add(block)


if (__name__ == "__main__"):
    pygame.init()
    window_size = window_width, window_height = 640, 480

    window = pygame.display.set_mode(window_size, pygame.RESIZABLE )
    pygame.display.set_caption("SideScroller")

    clock = pygame.time.Clock()
    frames_per_second = 60

    active_object_list = pygame.sprite.Group()
    player = Player()
    active_object_list.add(player)

    level_list = []
    level_list.append(Level_01(player))
    current_level_number = 0
    current_level = level_list[current_level_number]
    player.set_level(current_level)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update functions
        player.update(current_level.object_list, event)
        event = None
        current_level.update()

        # Logic Testing

        # Draw
        current_level.draw(window)
        active_object_list.draw(window)
        # Delay
        clock.tick(frames_per_second)
        # Update
        pygame.display.update()


    #window.blit(message, ( window_width - message.get_rect().width, 20))

    pygame.quit()


