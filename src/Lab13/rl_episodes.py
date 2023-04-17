'''
Lab 13: My first AI agent.
In this lab, you will create your first AI agent.
You will use the run_episode function from lab 12 to run a number of episodes
and collect the returns for each state-action pair.
Then you will use the returns to calculate the action values for each state-action pair.
Finally, you will use the action values to calculate the optimal policy.
You will then test the optimal policy to see how well it performs.


Sidebar-
If you reward every action you may end up in a situation where the agent
will always choose the action that gives the highest reward. Ironically,
this may lead to the agent losing the game.
'''
import sys
from pathlib import Path
from collections import defaultdict
import time




# line taken from turn_combat.py
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))


from lab11.pygame_combat import PyGameComputerCombatPlayer
from lab11.turn_combat import CombatPlayer
from lab12.episode import run_episode


from collections import defaultdict
import random
import numpy as np




class PyGameRandomCombatPlayer(PyGameComputerCombatPlayer):
    def __init__(self, name):
        super().__init__(name)


    def weapon_selecting_strategy(self):
        self.weapon = random.randint(0, 2)
        return self.weapon


class PyGamePolicyCombatPlayer(CombatPlayer):
    def __init__(self, name, policy):
        super().__init__(name)
        self.policy = policy


    def weapon_selecting_strategy(self):
        self.weapon = self.policy[self.current_env_state]
        return self.weapon


def run_random_episode(player, opponent):
    player.health = random.choice(range(10, 110, 10))
    opponent.health = random.choice(range(10, 110, 10))
    return run_episode(player, opponent)




def get_history_returns(history):
    total_return = sum([reward for _, _, reward in history])
    returns = {}
    for i, (state, action, reward) in enumerate(history):
        if state not in returns:
            returns[state] = {}
        returns[state][action] = total_return - sum(
            [reward for _, _, reward in history[:i]]
        )
    return returns




def run_episodes(n_episodes):
    ''' Run 'n_episodes' random episodes and return the action values for each state-action pair.
        Action values are calculated as the average return for each state-action pair over the 'n_episodes' episodes.
        Use the get_history_returns function to get the returns for each state-action pair in each episode.
        Collect the returns for each state-action pair in a dictionary of dictionaries where the keys are states and
            the values are dictionaries of actions and their returns.
        After all episodes have been run, calculate the average return for each state-action pair.
        Return the action values as a dictionary of dictionaries where the keys are states and
            the values are dictionaries of actions and their values.
    '''
    #Dictionaries
    historyDictionary = {}
    actionValues = {}
   
    #Loop for n_episodes
    print("STARTING GAME \n\n\n")
    for i in range(n_episodes):


        #Instantiate Players
        player = PyGameRandomCombatPlayer("Player")
        opponent = PyGameRandomCombatPlayer("Computer")


        #Get turn data, A tuple that contains [(player1_health,opponent_health),player_weapon,reward]
        turnData = run_random_episode(player,opponent)
        historyDictionary = get_history_returns(turnData)


        for state, innerDictionary in historyDictionary.items():


            if state not in actionValues:


                actionDictionary = {0: [], 1: [], 2: []}
                actionValues[state] = actionDictionary


            for action, reward in innerDictionary.items():
               
                actionValues[state][action].append(reward)
           
    ##Get averages
    for state, innerDictionary in actionValues.items():


        for action, reward in innerDictionary.items():


            #If there are rewards associated with an action
            if len(actionValues[state][action]) > 0:


                total = sum(actionValues[state][action])
                average = total/len(actionValues[state][action])


                actionValues[state][action] = average
            else:
                actionValues[state][action] = 0


    ##Delete unused keys (FROM CHAT GPT)
    ##I have a dictionary of dictionaries in python. The second dictionary values are list. Please write me code to loop and  delete all keys in the second dictionary where the values are empty lists##
    # Loop through the main dictionary
    for key in actionValues.keys():
        # Check if the key is present in the nested dictionary
        if key in actionValues and isinstance(actionValues[key], dict):
            nested_dict = actionValues[key]
            keys_to_delete = []
            for nested_key, nested_value in nested_dict.items():
                # Check if the value is an empty list
                if isinstance(nested_value, list) and not nested_value:
                    keys_to_delete.append(nested_key)
            # Delete keys with empty list values
            for key_to_delete in keys_to_delete:
                del actionValues[key][key_to_delete]
                print(f"Key '{key_to_delete}' deleted from dictionary '{key}'.")
        else:
            print(f"Nested dictionary not found for key '{key}'.")


    #I get the correct data structure I think. For some reason, when it's tested, I only get sword vs sword.
    print("Final Dictionary",actionValues)
    return actionValues


def get_optimal_policy(action_values):
    optimal_policy = defaultdict(int)
    for state in action_values:
        optimal_policy[state] = max(action_values[state], key=action_values[state].get)
    return optimal_policy


def test_policy(policy):
    names = ["Legolas", "Saruman"]
    total_reward = 0
    for _ in range(100):
        player1 = PyGamePolicyCombatPlayer(names[0], policy)
        player2 = PyGameComputerCombatPlayer(names[1])
        players = [player1, player2]
        total_reward += sum(
            [reward for _, _, reward in run_episode(*players)]
        )
    return total_reward / 100


if __name__ == "__main__":
    action_values = run_episodes(500)
    print(action_values)
    optimal_policy = get_optimal_policy(action_values)
    print(optimal_policy)
    print(test_policy(optimal_policy))





