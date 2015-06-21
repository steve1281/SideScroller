
import pygame

from properties import image_list, help_image, game_over_image

class ImageFactory():
   
    def __init__(self):
       self.images = {} 
       for i in image_list:
           self.images[i['name']] = self.makeImage(i['filename'],i['x'], i['y'])
       self.images['help'] = self.makeImage(help_image, 640, 400)
       self.images['gameover'] = self.makeImage(game_over_image, 640, 400)


    def makeImage(self, filename, x, y):
        return pygame.transform.scale(pygame.image.load(filename),(x, y))
  
    def getImage(self, name):
        return self.images[name]


