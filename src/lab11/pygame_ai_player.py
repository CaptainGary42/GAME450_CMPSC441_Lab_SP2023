import pygame
from lab11.turn_combat import CombatPlayer
import random
import time
import sys
from collections import deque



""" Create PyGameAIPlayer class here"""
class PyGameAIPlayer:
    def __init__(self) -> None:
        self.previous_city = 0
        pass

    def selectAction(self, state, cityConnections,endCity):


        #Select random city based of cities that are connected to the current city
        #print("CurrentCity",state.current_city)
        #print("City Connections",cityConnections)


        # Get list of accessible cities from current city
        accessibleCities = cityConnections[state.current_city]

        # Check if destination city is accessible

        if endCity in accessibleCities:
            return ord(str(endCity))

        # Calculate a weight for each accessible city based on its distance from the destination city
        cityWeights = {}
        for city in accessibleCities:
            distance = abs(city - state.destination_city)
            weight = 1 / (distance + 1)
            cityWeights[city] = weight

        # Normalize the weights to get a probability distribution
        totalWeight = sum(cityWeights.values())
        probabilities = {city: weight / totalWeight for city, weight in cityWeights.items()}

        randomCityChoice = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]
        #print("Random City Choice by AI: ",randomCityChoice)

        return ord(str(randomCityChoice))

        


        

     
       

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
            self.weapon = 2

        return self.weapon
