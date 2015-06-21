#!/usr/bin/env python
import sys
import time
import pygame
import getopt
from player import Player
from levelloader import LevelFile
from properties import window_width, window_height, MAXLEVEL, frames_per_second
from levelfactory import LevelFactory
from imagefactory import ImageFactory
from soundfactory import SoundFactory
from colors import CMap

class Game():

    def __init__(self):
        
        pygame.init()
        pygame.mixer.init()
        self.images = ImageFactory()
        self.sounds = SoundFactory()
        self.load_level()
        self.init_game()
        self.running_intro = False
        self.running_help = False
        self.running_game_over = False
        self.running_game = True
        self.running = True
        
  

    def init_game(self):

        self.window_size = window_width, window_height 
        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE )
        self.clock = pygame.time.Clock()
        self.frames_per_second = frames_per_second
        self.active_object_list = pygame.sprite.Group()
        self.player = Player()
        self.levels = LevelFactory(self.player)
        self.active_object_list.add(self.player)
        self.change_to_level(self.levelnumber)

    def change_to_level(self, levelnumber):
        self.levelnumber = levelnumber
        self.current_level_number = self.levelnumber
        self.current_level = self.levels.getLevel(levelnumber)
        self.player.set_level(self.current_level)
        pygame.display.set_caption(self.current_level.get_level_name())

    def run(self):
        self.locked = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_SPACE and self.running_game:
                        # todo: remove the space option
                        self.current_level_number =  (self.current_level_number + 1) % MAXLEVEL
                        self.change_to_level(self.current_level_number)
                    if event.key == pygame.K_h and self.running_game:
                        self.running_game = False
                        self.running_help = True
                    if event.key == pygame.K_SPACE and self.running_help:
                        self.running_game = True
                        self.running_help = False
                    if event.key == pygame.K_SPACE and self.running_game_over:
                        self.running = False
                        continue
                  
            # determine where we are visa-v game state
            if self.running_game: 
                # Update functions
                self.player.update(self.current_level.object_list, event)
                # - check for exit collision
                if self.locked == False and self.player.did_collide(\
                   self.current_level.exit_list, event):
                    self.sounds.getSound("woosh").play()
                    self.current_level_number =  self.current_level_number + 1
		    if self.current_level_number == MAXLEVEL:
                        self.running_game = False
                        self.running_game_over = True 
                        continue
                    else:
                        self.change_to_level(self.current_level_number)
                        self.locked = True

                x = self.player.did_collide(self.current_level.key_list, event)
                if x:
                    self.current_level.key_list = \
                        [item for item in self.current_level.key_list if item not in x]
                    self.locked = False
                    sounda = self.sounds.getSound("glass_ding")
                    sounda.play()

                if self.player.did_collide(self.current_level.cat_list, event):
                    sounda = self.sounds.getSound("meow")
                    sounda.play()

                event = None
                self.current_level.update()

                # Logic Testing
                self.current_level.run_viewbox()
                # Draw
                self.current_level.draw(self.window)
                self.active_object_list.draw(self.window)
            elif self.running_help:
                self.window.fill(CMap.blue)
                self.window.blit(self.images.getImage('help'),(0,0))
            elif self.running_intro:
                pass
            elif self.running_game_over:
                self.window.fill(CMap.blue)
                self.window.blit(self.images.getImage('gameover'),(0,0))
            else:
                pass

            # Delay
            self.clock.tick(self.frames_per_second)
            # Update
            pygame.display.update()

        pygame.quit()

    def load_level(self):
        self.levelnumber = -1
        try:
            opts, args = getopt.getopt(sys.argv[1:],"hl:","level=")
        except getopt.GetoptError:
            print 'levelbuilder.py -l <levelnumber>'
            sys.exit(2)
        # -l
        for opt, arg in opts:
            if opt == '-h':
                print 'levelbuilder.py -l <levelnumber>'
                sys.exit()
            elif opt in ("-l", "--level"):
                self.levelnumber = int(arg)
        if self.levelnumber == -1:
            self.levelnumber = 0

if (__name__ == "__main__"):
    (Game()).run()
