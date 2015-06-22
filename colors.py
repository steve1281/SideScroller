import pygame

class CMap():
    # class exposed
    white = pygame.Color(255, 255, 255),
    black = pygame.Color(0, 0, 0),
    gray = pygame.Color(90, 90, 90),
    silver = pygame.Color(200, 200, 200),
    red = pygame.Color(255, 0, 0),
    blue =  pygame.Color(0, 0, 255),
    green = pygame.Color(0, 255, 0),
    yellow = pygame.Color(255, 255, 0),
    purple = pygame.Color(221,160,221),

    def __init__(self):
        self.color_map = {
            'white' : CMap.white ,
            'black' : CMap.black,
            'gray' : CMap.gray,
            'silver' : CMap.silver,
            'red' : CMap.red,
            'blue' : CMap.blue,
            'green' : CMap.green,
            'yellow' : CMap.yellow,
            'purple' : CMap.purple,
        }

    def decode(self, code):
        return self.color_map[code]

    def recode(self, col):
        for m,c in self.color_map.iteritems():
            if c == col:
                return m
        return 'black'


    
