
from levelloader import LevelFile
from properties import level_file_list

"""
    This class loads the level once and only once.
"""
class LevelFactory():

    def __init__(self, player):
       self.levels = []
       for level in level_file_list:
           self.levels.append(LevelFile(player, level))

    def getLevel(self, level_number):
       level =  self.levels[level_number]
       level.reset()
       return level

    
