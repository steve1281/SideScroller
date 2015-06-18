#!/usr/bin/env python
import sys
import pygame
import getopt
from player import Player
from levelloader import LevelFile
from properties import window_width, window_height, MAXLEVEL


class Game():

    def __init__(self):
        self.load_level()
        self.init_game()

    def init_game(self):
        pygame.init()
        self.window_size = window_width, window_height #= 640, 480

        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE )
        pygame.display.set_caption("Side Scroller")

        self.clock = pygame.time.Clock()
        self.frames_per_second = 60

        self.active_object_list = pygame.sprite.Group()
        self.player = Player()
        self.active_object_list.add(self.player)

        self.current_level_number = self.levelnumber
        self.current_level = LevelFile(self.player, 'data/level0'+str(self.levelnumber)+".dat")
        self.player.set_level(self.current_level)

    def run(self):
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
                        self.current_level = LevelFile(self.player, 'data/level0' \
                            +str(self.current_level_number)+".dat")
                        self.player.set_level(self.current_level)

            # Update functions
            self.player.update(self.current_level.object_list, event)
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
