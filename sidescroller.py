#!/usr/bin/env python
import sys
import pygame
import getopt
from player import Player
from levelloader import LevelFile
from properties import window_width, window_height, MAXLEVEL, frames_per_second

class Game():

    def __init__(self):
        self.load_level()
        self.init_game()

    def init_game(self):
        pygame.init()
        self.window_size = window_width, window_height 
        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE )
        self.clock = pygame.time.Clock()
        self.frames_per_second = frames_per_second
        self.active_object_list = pygame.sprite.Group()
        self.player = Player()
        self.active_object_list.add(self.player)
        self.change_to_level(self.levelnumber)

    def change_to_level(self, levelnumber):
        self.levelnumber = levelnumber
        self.current_level_number = self.levelnumber
        self.current_level = LevelFile(self.player, 'data/level0'+str(self.levelnumber)+".dat")
        self.player.set_level(self.current_level)
        pygame.display.set_caption(self.current_level.get_level_name())

    def run(self):
        self.locked = True
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_SPACE:
                        self.current_level_number =  (self.current_level_number + 1) % MAXLEVEL
                        self.change_to_level(self.current_level_number)

            # Update functions
            self.player.update(self.current_level.object_list, event)
            # - check for exit collision
            if self.locked == False and self.player.did_collide(self.current_level.exit_list, event):
                self.current_level_number =  (self.current_level_number + 1) % MAXLEVEL
                self.change_to_level(self.current_level_number)
                self.locked = True

            x = self.player.did_collide(self.current_level.key_list, event)
            if x:
                self.current_level.key_list = [item for item in self.current_level.key_list if item not in x]
                self.locked = False
                

            event = None
            self.current_level.update()

            # Logic Testing
            self.current_level.run_viewbox()
            # Draw
            self.current_level.draw(self.window)
            self.active_object_list.draw(self.window)
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
