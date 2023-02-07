'''
Lab 5: PCG and Project Lab

This a combined procedural content generation and project lab. 
You will be creating the static components of the game that will be used in the project.
Use the landscape.py file to generate a landscape for the game using perlin noise.
Use the lab 2 cities_n_routes.py file to generate cities and routes for the game.
Draw the landscape, cities and routes on the screen using pygame.draw functions.
Look for triple quotes for instructions on what to do where.
The intention of this lab is to get you familiar with the pygame.draw functions, 
use perlin noise to generate a landscape and more importantly,
build a mindset of writing modular code.
This is the first time you will be creating code that you may use later in the project.
So, please try to write good modular code that you can reuse later.
You can always write non-modular code for the first time and then refactor it later.
'''

import sys
import pygame
import random
import numpy as np
from landscape import get_landscape

from pathlib import Path
sys.path.append(str((Path(__file__)/'..'/'..').resolve().absolute()))
from lab2.cities_n_routes import get_randomly_spread_cities, get_routes


# TODO: Demo blittable surface helper function

''' Create helper functions here '''

""""
>generate the map 
>
"""

def generateSurface(size):
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3]) 

    return pygame_surface

""""
>get the randomly generated cities coordinates
>
"""
def getCityLocations(size, numCities):
    return get_randomly_spread_cities(size, numCities)

""""
>get the routes (tuples) between cities
>
"""
def getRoutes(city_names):
    return get_routes(city_names)


""""
>drawCities
>Draw the cities on the map as orange dors
"""
def drawCities(city_locations,surface):
    orange = 255,102,0
    for x in city_locations:
        pygame.draw.circle(surface,orange,(x[0],x[1]),10)

""""
>drawRoutes
>Draw the roads between the cities
"""

def drawRoutes(routes,dict,surface):
    grey = 58,58,58

    for x in routes:
        cityA = x[0]
        cityB = x[1]
        pygame.draw.line(surface,grey,dict[cityA],dict[cityB],5)


if __name__ == "__main__":
    pygame.init()
    size = width, height = 640, 480
    black = 1, 1, 1

    screen = pygame.display.set_mode(size)

    
    pygame_surface = generateSurface(size)
    city_names = ['Morkomasto', 'Morathrad', 'Eregailin', 'Corathrad', 'Eregarta',
                  'Numensari', 'Rhunkadi', 'Londathrad', 'Baernlad', 'Forthyr']

 
    ''' Setup cities and routes in here'''
    city_locations = getCityLocations(size, 10)
    routes = getRoutes(city_names)

    city_locations_dict = {name: location for name, location in zip(city_names, city_locations)}
    random.shuffle(routes)
    routes = routes[:10] 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(black)
        screen.blit(pygame_surface, (0, 0))

        
        drawRoutes(routes,city_locations_dict,pygame_surface)
        drawCities(city_locations,pygame_surface)

        pygame.display.flip()
