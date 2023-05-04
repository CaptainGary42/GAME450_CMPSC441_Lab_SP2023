import sys
import pygame
import random
import numpy as np
from sprite import Sprite

from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from landscape import get_landscape, get_combat_bg
from pygame_ai_player import PyGameAIPlayer
from lab5.game_world_gen_practice import drawCities,drawRoutes 
from lab5.landscape import elevation_to_rgba, get_elevation
from lab7.ga_cities import game_fitness,setup_GA,solution_to_cities
from lab2.cities_n_routes import get_randomly_spread_cities, get_routes
from lab3.travel_cost import get_route_cost

import openai
import requests
from PIL import Image
from io import BytesIO
import os
import time



from pathlib import Path
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))



pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)

#Compute elevation array map to a pygame surface
def get_landscape_surface(size,elevation):

  
    landscape = elevation_to_rgba(elevation)

    print("Created a world landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface

def get_combat_surface(size):
    landscape = get_combat_bg(size)
    print("Created a combat landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width, height, caption):
    pygame.init()
    print(type(caption))
    window = pygame.display.set_mode((width, height))
    return window



def displayCityNames(city_locations, city_names):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])

def endGame(state):

    if(state == 1):
        print("You survived and reached the end!")
        generateEndImage(state)
    if(state == 2):
        print("You ran out of money and starved.")
        generateEndImage(state)
    if(state == 3):
        print("You were violently killed. :( ")
        generateEndImage(state)

    print("Thanks for playing!")
    time.sleep(1)
    pygame.quit()

def createCityDictionary(routes,cities):
        
        cityConnections = {i: [] for i in range(len(cities))}

        # Loop through each route
        for route in routes:
            # Find the indices of the two cities in the route
            city1_index = np.where((cities == route[0]).all(axis=1))[0][0]
            city2_index = np.where((cities == route[1]).all(axis=1))[0][0]
            
            # Add the indices of the connected cities to each city's value list in the dictionary
            cityConnections[city1_index].append(city2_index)
            cityConnections[city2_index].append(city1_index)
    
        return cityConnections


def connectIsolatedCities(cities,routes):

    
    isolatedCities = []
    notIsolatedCities = []

    for city in cities:
        found = False
        for route in routes:
            if (city == route[0]).all() or (city == route[1]).all():
                found = True
                notIsolatedCities.append(city)
                break
        if not found:
            isolatedCities.append(city)

    for city in isolatedCities:
        random_city = random.choice(notIsolatedCities)
        routes.append((city, random_city))
     

    return routes
    


def getEndCity(cityConnections):
    # Start at city 0
    current_city = 0

    # Initialize a dictionary to keep track of the cityConnections to each city
    distances = {city: float('inf') for city in cityConnections}
    distances[0] = 0

    # Initialize a dictionary to keep track of the number of connections to reach each city
    connections = {city: 0 for city in cityConnections}

    # Breadth-first search to find the farthest city from the starting point
    queue = [current_city]
    while queue:
        current_city = queue.pop(0)
        for neighbor in cityConnections[current_city]:
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distances[current_city] + 1
                connections[neighbor] = connections[current_city] + 1
                queue.append(neighbor)

    # Find the city with the most connections that is farthest from the starting point
    farthest_city = max([(city, connections[city]) for city in cityConnections if connections[city] > 0], key=lambda x: (distances[x[0]], x[1]))[0]

    # Print the results
    print("The farthest city from the starting point that takes the most connections to get to is:", farthest_city)

    return farthest_city

def generateEndImage(state):

    # Authenticate with the OpenAI API
    openai.api_key = "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"

    #Get prompt depending on state
    if(state == 1):
        print("You survived and reached the end!")
        PROMPT = "An elf standing victorious on a hill, overlooking a village in front of a sunset."
    if(state == 2):
        PROMPT ="An elf dressed in rags and starving."
    if(state == 3):
        PROMPT = "A elf defeated in battle"


    response = openai.Image.create(prompt=PROMPT,n=1,size="256x256")

    imageURL = response["data"][0]["url"]

    #Display the generated image
    image_content = requests.get(imageURL).content
    image = Image.open(BytesIO(image_content))
    image.show()



class State:
    def __init__(
        self, gameStatus,money, victoryStatus, current_city, destination_city, travelling, encounter_event, cities, routes
    ):
        self.gameStatus = gameStatus
        self.money = money
        self.victoryStatus = victoryStatus
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes
       


#Run the game
if __name__ == "__main__":
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 0
    sprite_path = "assets/lego.png"
    sprite_speed = 1

    #Set up the game screen
    screen = setup_window(width, height, "Game World Gen Practice")

    #Get a random elevation map
    elevation = get_elevation(size)

    #Get landscape surface
    landscape_surface = get_landscape_surface(size,elevation)

    #Get combat surface
    combat_surface = get_combat_surface(size)

    #Name cities (Maybe have AI generate?)
    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    #Get random cities
    cities = get_randomly_spread_cities(size, len(city_names))

    # setup fitness function and genetic algorithm
    fitness = lambda cities, idx: game_fitness(
        cities, idx, elevation=elevation, size=size
    )
    fitness_function, ga_instance = setup_GA(fitness, 10, size)

    #Run genetic algorithm
    ga_instance.run()
    ga_instance.plot_fitness()

    #Get better placed cities
    cities = ga_instance.initial_population[0]
    cities = solution_to_cities(cities, size)
    #print("Cities",cities)
    

    #Get routes between cities
    routes = get_routes(cities)

    #Get only 10 routers
    random.shuffle(routes)
    routes = routes[:10]
    #print("Selected Routes",routes)
    
    #Connect Isolated Cities
    connectIsolatedCities(cities,routes)

    #Create player sprite
    player_sprite = Sprite(sprite_path, cities[start_city])


    #UNCOMMENT THIS TO INSTANTIATE THE HUMAN PLAYER AND PlAY NORMALLY
    #Instantiate Human Player
    #player = PyGameHumanPlayer()


    """ Add a line below that will reset the player variable to 
    a new object of PyGameAIPlayer class."""
    #Instantiate AI Player
    player = PyGameAIPlayer()
    """"""

    state = State(
        gameStatus=False,
        money=(300),
        victoryStatus = -1,
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
    )

    #Get a dicitionary of all the city connections
    cityConnections = createCityDictionary(routes,cities)

    #Get the destination city
    endCity  = getEndCity(cityConnections)

    victoryStatus = -1

    #time.sleep(3)
    while True:

        #Get the player input
        action = player.selectAction(state,cityConnections, endCity)

        #If the player chooses a city that's not accessible from their position, continue.
        if(action == -1):
            continue

        #If the player choice is within 0 and 9
        if 0 <= int(chr(action)) <= 9:

            #If the player's choice isn't their current position
            if int(chr(action)) != state.current_city and not state.travelling:

                #Set the starting city
                start = cities[state.current_city]

                state.destination_city = int(chr(action))

                #Set the destination city
                destination = cities[state.destination_city]

                #Calculate the amount of money the player will spend to travel
                #print("RouteCoordinate",(tuple(start),tuple(destination)))
                costToTravel = round(get_route_cost((tuple(start),tuple(destination)),elevation))
                print("Cost to travel",costToTravel)
                print("Money before spending",state.money)

              
                #Decrease money
                state.money-=costToTravel

                print("Money after spending",state.money)

                player_sprite.set_location(cities[state.current_city])
                state.travelling = True

                #End the game if the player runs out of money
                if((state.money) <= 0):
                    endGame(2)


        #Clear the game world surface
        screen.fill(black)

        screen.blit(landscape_surface, (0, 0))

        #Draw the cities as dots on the game world surface
        drawCities(cities,landscape_surface)

        #Draw the routes between the cities
        for line in routes:
            pygame.draw.line(screen, (128, 128, 128), *line)

        #Display the names of the cities (including the number)
        displayCityNames(cities, city_names)

        #If the player is traveling to another city
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2

        #If the player is not traveling to another city
        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        #If combat occurs
        if state.encounter_event:
            state.victoryStatus = run_pygame_combat(combat_surface, screen, player_sprite)
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()


        #Checks if the player lost the fight
        if(state.victoryStatus == 0):
            endGame(3)
        

        #If the player reaches has reached the end city
        if(state.current_city == endCity):
            endGame(1)


