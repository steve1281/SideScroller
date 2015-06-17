#!/usr/bin/env python
import sys
import pygame
import json
import getopt

from colors import *
from player import Player
from levelloader import LevelFile
from block import Block

from properties import (window_width, window_height)


if (__name__ == "__main__"):
    levelnumber = -1
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
            levelnumber = int(arg)

    if levelnumber == -1:
        levelnumber = 0

    pygame.init()
    window_size = window_width, window_height #= 640, 480

    window = pygame.display.set_mode(window_size, pygame.RESIZABLE )
    pygame.display.set_caption("Side Scroller")

    clock = pygame.time.Clock()
    frames_per_second = 60

    active_object_list = pygame.sprite.Group()
    player = Player()
    active_object_list.add(player)

    level_list = []
    level_list.append(LevelFile(player, 'data/level01.dat'))
    level_list.append(LevelFile(player, 'data/level02.dat'))
    level_list.append(LevelFile(player, 'data/level03.dat'))
    level_list.append(LevelFile(player, 'data/level04.dat'))
    current_level_number = levelnumber
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


