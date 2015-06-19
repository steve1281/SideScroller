#!/usr/bin/env python

import sys
import pygame
import json
from colors import *
from player import Player
from block import Block
from properties import window_width, window_height

class Level(object):
    def __init__(self, player_object):
        self.init_viewbox(player_object)

    def init_viewbox(self, player_object):
        self.object_list = pygame.sprite.Group()
        self.exit_list = pygame.sprite.Group()
        self.key_list = pygame.sprite.Group()
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
        self.exit_list.draw(window)
        if self.key_list:
            self.key_list.draw(window)

    def shift_world(self, shift_x, shift_y):
        self.world_shift_x += shift_x
        self.world_shift_y += shift_y
        for each_object in self.object_list:
            each_object.rect.x += shift_x
            each_object.rect.y += shift_y
        for each_object in self.exit_list:
            each_object.rect.x += shift_x
            each_object.rect.y += shift_y
        for each_object in self.key_list:
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

class LevelFile( Level ):
    def __init__(self, player_object, filename):
        super(LevelFile, self).__init__(player_object)
        self.load(filename)
        self.player_start_x = self.data['playerstart'][0]
        self.player_start_y = self.data['playerstart'][1] 
        self.player_start = self.player_start_x, self.player_start_y   
        level = self.data['blocks']
        for block in level:
            block = Block( block[0], block[1], block[2], block[3], black )
            self.object_list.add(block)
        block = Block( self.data['exit'][0], self.data['exit'][1]-25, 30, 50, red)
        self.exit_list.add(block)
        block = Block( self.data['key'][0], self.data['key'][1]-25, 30, 50, yellow)
        self.key_list.add(block)
    
    def get_level_name(self):
        return self.data['meta']['levelname']

    def get_level_exit(self):
        return self.data['exit']

    def get_level_key(self):
        return self.data['key']

    def load(self, filename):
        """ Read in level file 
        """
        try:
            with open(filename) as data_file:
                self.data = json.load(data_file)
        except IOError:
            print "Error: %s was not found." % filename
            sys.exit(2)

