import pygame
from lab11.turn_combat import CombatPlayer


class PyGameHumanPlayer:
    def __init__(self):
        pass

    def selectAction(self, state, cityConnections):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if ord("0") <= event.key <= ord("9"):
                    if int(chr(event.key)) in cityConnections[state.current_city]:
                        #print("key",int(chr(event.key)))
                        #print("accessible")
                        #print("accessibleCities",cityConnections[state.current_city])
                        return event.key
                    else:
                        #print("not accessible")
                        #print("accessibleCities",cityConnections[state.current_city])
                        return -1
        return ord(str(state.current_city))  # Not a safe operation for >10 cities


class PyGameHumanCombatPlayer(CombatPlayer):

    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [ord("s"), ord("a"), ord("f")]:
                        choice = {ord("s"): 1, ord("a"): 2, ord("f"): 3}[event.key]
                        self.weapon = choice - 1
                        return self.weapon
