#!/usr/bin/env python
import math
import pygame
import sys
import getopt
import json
from imagefactory import ImageFactory

from colors import CMap



class LevelBuilder:
    def __init__(self):
        self.images = ImageFactory()

    def load(self,argv):
        """ load level from a file or throw an error.
        """
        filename =  ""
        levelname = ""
        try:
            opts, args = getopt.getopt(argv,"hf:l:","file=,levelname=")
        except getopt.GetoptError:
            print 'levelbuilder.py -f <levelfile> -l <levelname>'
            sys.exit(2)
        # -l, -f, -h
        for opt, arg in opts:
            if opt == '-h':
                print 'levelbuilder.py -f <levelfile>'
                sys.exit()
            elif opt in ("-f", "--file"):
                filename = arg
            elif opt in ("-l", "--levelname"):
                levelname = arg

        # if the filename was not set, abort
        if filename == "":
            print "levelbuilder.py -f <levelfile>"
            sys.exit(2)


        # read the file in, if any.
        try:
            with open(filename) as data_file:
                data = json.load(data_file)
            print "Using %s." % filename
        except IOError:
            print "Creating new file %s. " % filename
            data = {}

        # basic save level structure. It we decide to add new stuff
        # this will add it in with a default
        data.setdefault('meta',{}).setdefault('version', 0)
        data.setdefault('meta',{}).setdefault('levelname', "levelname")
        data.setdefault('blocks',[])
        data.setdefault('playerstart', (0,0))
        data.setdefault('key', (0,0))
        data.setdefault('exit' ,(0,0))
        data.setdefault('cat' ,(0,0))
        # set members
        self.data=data
        self.filename = filename
        self.levelname = levelname


    def save(self):
        """ write out the level.
        """
        data = self.data
        #increase the version of the file by one.
        data.setdefault('meta',{})['version'] += 1

        # set a levelname if one is provided.
        if self.levelname != "":
            data.setdefault('meta',{})['levelname'] = self.levelname

        with open(self.filename, 'w') as outfile:
            json.dump(data, outfile)


    def main(self):
        self.load(sys.argv[1:])
        to_draw = []
        for r in self.data['blocks']:
            to_draw.append((pygame.Rect((r[0],r[1]),(r[2], r[3])), (CMap()).decode(r[4])))

        pygame.init()

        size = width, height = 1200, 1000
        window = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        fps = 60
        window.fill(CMap.white)
        pygame.display.update()

        draw_start_box = False
        current_color = CMap.silver
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                   event.type == pygame.KEYDOWN and \
                   event.key == pygame.K_ESCAPE:
                    running = False
                elif (event.type == pygame.MOUSEMOTION):
                    mouse_pos = mouse_x, mouse_y = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.data['playerstart'] = pygame.mouse.get_pos()
                        event = None
                    else:
                        rpos = mouse_pos
                        sx = math.floor(rpos[0]/10)*10
                        sy = math.floor(rpos[1]/10)*10
                        pos = (sx,sy)
                        for itemx in to_draw:
                            item = itemx[0]
                            col = itemx[1]
                            if item.collidepoint(pos):
                                pygame.draw.rect(window, CMap.red, item)
                            else:
                                pygame.draw.rect(window, col, item)
                                draw_start_box = True
                elif event.type == pygame.MOUSEBUTTONUP:
	            if event.button == 3:
		        event = None
		    else:
                        rpos = mouse_pos
                        sx = math.floor(rpos[0]/10)*10
                        sy = math.floor(rpos[1]/10)*10
                        final_pos = (sx,sy)

                        #final_pos = mouse_pos
                        draw_start_box = False
                        r = pygame.Rect(pos, (final_pos[0]-pos[0], final_pos[1]-pos[1]))
                        r.normalize()
                        to_draw.append((r,current_color))

                        

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        temp = []
                        for p in to_draw:
                            platform = p[0]
                            col = p[1]
                            if platform.width < 1 and platform.height < 1:
                                pass
                            else:
                               temp.append((platform.left,platform.top,platform.width,\
                                   platform.height,(CMap()).recode(col)))
                        self.data['blocks'] = temp
                        self.save()

                    if event.key == pygame.K_BACKSPACE:
                        if len(to_draw):
                            to_draw.pop()
                    if event.key == pygame.K_e:
                         pos = pygame.mouse.get_pos()
                         self.data['exit'] = pos
                    if event.key == pygame.K_k:
                         pos = pygame.mouse.get_pos()
                         self.data['key'] = pos
                    if event.key == pygame.K_c:
                         pos = pygame.mouse.get_pos()
                         self.data['cat'] = pos
                    if event.key == pygame.K_0:
                         current_color = CMap.black
                    if event.key == pygame.K_1:
                         current_color = CMap.gray
                    if event.key == pygame.K_2:
                         current_color = CMap.silver
                    if event.key == pygame.K_3:
                         current_color = CMap.red
                    if event.key == pygame.K_4:
                         current_color = CMap.blue
                    if event.key == pygame.K_5:
                         current_color = CMap.green
                    if event.key == pygame.K_6:
                         current_color = CMap.yellow
                    if event.key == pygame.K_7:
                         current_color = CMap.purple

                    

            window.fill(CMap.white)
            pygame.draw.rect(window, current_color, pygame.Rect( (0,0),(20,20)))
            if (draw_start_box):
                pygame.draw.rect(window, CMap.red, pygame.Rect(pos, \
                   (mouse_pos[0]-pos[0], mouse_pos[1]-pos[1])))

            for item in to_draw:
                if len(item) >1:
                    pygame.draw.rect(window, item[1], item[0])

            if self.data['playerstart']:
                window.blit( self.images.getImage('standing'), \
                    (self.data['playerstart'][0], self.data['playerstart'][1] -25))

            if self.data['exit']:
                window.blit( self.images.getImage('exit'), \
                    (self.data['exit'][0] , self.data['exit'][1] -25))

            if self.data['key']:
                window.blit( self.images.getImage('key'), \
                    (self.data['key'][0] , self.data['key'][1] -25))

            if self.data['cat']:
                window.blit( self.images.getImage('cat'), \
                    (self.data['cat'][0] -30, self.data['cat'][1] -25))

            pygame.display.update()
            clock.tick(fps)

        pygame.quit()

        
if  __name__ == "__main__":
    (LevelBuilder()).main()

