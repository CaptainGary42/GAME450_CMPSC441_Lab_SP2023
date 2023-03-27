import pygame
from lab11.turn_combat import CombatPlayer
import random
import time

""" Create PyGameAIPlayer class here"""
class PyGameAIPlayer:
    def __init__(self) -> None:
        pass

    def selectAction(self, state):
        start = state.current_city
        if(start+1 > 9):
            return ord(str(9))
        return ord(str(start+1))
       
    


""" Create PyGameAICombatPlayer class here"""
class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name, roundcount):
        super().__init__(name)
        self.roundcount = roundcount

    def weapon_selecting_strategy(self):

        if(self.roundcount < 5):
            self.weapon =1
            self.roundcount+=1
            return self.weapon
        if(self.roundcount > 5 and self.roundcount < 8):
            self.weapon = 0
            self.roundcount+=1
            return self.weapon
        else:
            self.roundcount+=1
            self.weapon = random.randint(0,2)

        return self.weapon
