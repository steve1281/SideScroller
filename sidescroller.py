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
        self.world_shift_x = 0
        self.world_shift_y = 0
        self.left_viewbox = window_width//2 - window_width/8
        self.right_viewbox = window_width//2 - window_width/10
        self.up_viewbox = window_height/4
        self.down_viewbox = window_height/2 + window_height/12

    def update(self):
        self.object_list.update()

    def draw(self, window):
        window.fill(white)
        self.object_list.draw(window)

    def shift_world(self, shift_x, shift_y):
        self.world_shift_x += shift_x
        self.world_shift_y += shift_y

        for each_object in self.object_list:
            each_object.rect.x += shift_x
            each_object.rect.y += shift_y

    def run_viewbox(self):
        if self.player_object.rect.x <= self.left_viewbox:
            view_difference  = self.left_viewbox - self.player_object.rect.x
            self.player_object.rect.x = self.left_viewbox
            self.shift_world(view_difference, 0)
        if self.player_object.rect.x > self.right_viewbox:
            view_difference  = self.right_viewbox - self.player_object.rect.x
            self.player_object.rect.x = self.right_viewbox
            self.shift_world(view_difference, 0)
        if self.player_object.rect.y <= self.up_viewbox:
            view_difference  = self.up_viewbox - self.player_object.rect.y
            self.player_object.rect.y = self.up_viewbox
            self.shift_world(0, view_difference)
        if self.player_object.rect.y >  self.down_viewbox:
            view_difference  = self.down_viewbox - self.player_object.rect.y
            self.player_object.rect.y = self.down_viewbox
            self.shift_world(0, view_difference)

class Level_File( Level ):
    def __init__(self, player_object, filename):
        super(Level_File, self).__init__(player_object)
        load(filename)
        self.player_start = self.player_start_x, self.player_start_y = self.data['playerstart'][0], self.data['playerstart'][1]
        level = self.data['blocks']
        for block in level:
            block = Block( block[0], block[1], block[2], block[3], block[4])
            self.object_list.add(block)

    def load(self, filename):
        """ Read in level file 
        """
        try:
            with open(filename) as data_file:
                data = json.load(data_file)
            print "Using %s." % filename
        except IOError:
            print "Error: %s was not found." % filename
            sys.exit(2)



class Level_03( Level):
    def __init__(self, player_object):
        super(Level_03, self).__init__(player_object)
        self.player_start = self.player_start_x, self.player_start_y = 91, 68
        level = [
            [10, 10, 1180, 30, black],
            [10, 40, 30, 780, black],
            [30, 790, 1140, 30, black],
            [1160, 40, 30, 780, black],
            [70, 100, 130, 30, black],
            [170, 120, 100, 30, black],
            [250, 150, 110, 30, black],
            [320, 170, 120, 40, black],
            [80, 270, 350, 30, black],
            [90, 380, 340, 20, black],
            [110, 470, 480, 20, black],
            [220, 590, 430, 20, black],
            [650, 130, 20, 480, black],
            [660, 220, 150, 20, black],
            [820, 330, 180, 40, black],
            [960, 500, 160, 40, black],
            [790, 600, 170, 40, black],
            [930, 700, 160, 30, black],
            [310, 730, 200, 20, black],
            [980, 140, 180, 30, black],
        ]
        for block in level:
            block = Block( block[0], block[1], block[2], block[3], block[4])
            self.object_list.add(block)


class Level_02( Level):
    def __init__(self, player_object):
        super(Level_02, self).__init__(player_object)
        self.player_start = self.player_start_x, self.player_start_y = 138, 108

	level = [
	    [489, 155, 0, 0, black],
	    [54, 38, 1095, 20, black],
	    [54, 56, 19, 861, black],
	    [72, 894, 1077, 22, black],
	    [1148, 38, 17, 878, black],
	    [487, 362, 225, 21, black],
	    [487, 382, 25, 169, black],
	    [510, 522, 200, 28, black],
	    [694, 386, 26, 163, black],
	    [695, 366, 18, 24, black],
	    [711, 364, 5, 27, black],
	    [113, 150, 179, 33, black],
	    [252, 182, 69, 29, black],
	    [298, 209, 74, 31, black],
	    [355, 238, 80, 31, black],
	    [419, 273, 67, 34, black],
	    [421, 265, 64, 13, black],
	    [73, 409, 233, 34, black],
	    [247, 612, 184, 31, black],
	    [757, 609, 193, 37, black],
	    [753, 249, 259, 39, black],
	    [500, 737, 222, 49, black],
	]
        for block in level:
            block = Block( block[0], block[1], block[2], block[3], block[4])
            self.object_list.add(block)

class Level_01( Level):
    def __init__(self,player_object):
        super(Level_01, self).__init__(player_object)
        self.player_start = self.player_start_x, self.player_start_y = 100, 100

        level = [
	    [16, 15, 1178, 20, black],
	    [17, 15, 23, 971, black],
	    [18, 966, 1172, 20, black],
	    [1173, 33, 21, 948, black],
	    [39, 133, 354, 28, black],
	    [407, 237, 417, 32, black],
	    [849, 130, 327, 31, black],
	    [110, 440, 279, 25, black],
	    [550, 440, 325, 24, black],
	    [1044, 434, 134, 25, black],
	    [278, 588, 348, 34, black],
	    [811, 595, 284, 28, black],
	    [39, 742, 248, 28, black],
	    [473, 738, 704, 30, black],
        ]
        for block in level:
            block = Block( block[0], block[1], block[2], block[3], block[4])
            self.object_list.add(block)


if (__name__ == "__main__"):
    pygame.init()
    window_size = window_width, window_height = 640, 480

    window = pygame.display.set_mode(window_size, pygame.RESIZABLE )
    pygame.display.set_caption("Side Scroller")

    clock = pygame.time.Clock()
    frames_per_second = 60

    active_object_list = pygame.sprite.Group()
    player = Player()
    active_object_list.add(player)

    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))
    current_level_number = 2
    current_level = level_list[current_level_number]
    #player.set_level(current_level)

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
        current_level.run_viewbox()
        # Draw
        current_level.draw(window)
        active_object_list.draw(window)
        # Delay
        clock.tick(frames_per_second)
        # Update
        pygame.display.update()

    pygame.quit()


