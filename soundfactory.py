import pygame
from properties import sound_list

class SoundFactory():
    def __init__(self):
        self.sounds = {}
        for i in sound_list:
            self.sounds[i['name']] = self.makeSound(i['filename'])
    
    def makeSound(self, filename):
        return pygame.mixer.Sound(filename)
    
    def getSound(self, name):
        return self.sounds[name]

