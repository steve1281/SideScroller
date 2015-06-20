
import pygame

from properties import image_list

class ImageFactory():
   
    def __init__(self):
       self.images = {} 
       for i in image_list:
           self.images[i['name']] = self.makeImage(i['filename'],30, 50)

    def makeImage(self, filename, x, y):
        return pygame.transform.scale(pygame.image.load(filename),(x, y))
  
    def getImage(self, name):
        return self.images[name]


