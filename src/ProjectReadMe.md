Project Abstract

This programming project is based on the story of a young elf named Oillill who sets out on a journey to the distant city of Evereska to seek opportunities and build a better life. The project involves developing a game that simulates this journey, where the player takes on the role of Oillill and must travel through a randomly generated world to reach the destination city. The game incorporates several AI techniques, such as genetic algorithms, AI players, and text-to-image generation models, to create a challenging and immersive gaming experience.
The game map is generated using perlin noise, and the locations of the cities are tweaked with a genetic algorithm to make them more realistically displaced. The player must navigate through different paths that have varying costs depending on their elevation and distance. The game also includes a battle sequence, where the player can trigger an encounter with an AI enemy and engage in a version of rock-paper-scissors to defeat it.
The player starts the game with a set amount of money and must manage it throughout the journey. If the player runs out of money, they will starve and lose the game.
In order to win the game, the player must reach their destination city without running out of money or losing a battle.

The purpose of this project is to demonstrate proficiency in Python, problem-solving, and implementing AI techniques. It’s also intended to provide a fun and engaging gaming experience for players who enjoy strategy and adventure games.


List of AI Components:

AI Player
Genetic Algorithm
Text-to-Image Generation

Problems Solved

AI PLAYER: 

I have developed an AI player for this game, overcoming two main challenges - determining where to go and winning fights. Initially, I focused on enhancing its fighting ability by utilizing my knowledge of the opponent's behavior. Since the computer AI makes decisions based on its health, I leveraged this to my advantage. Recognizing that the enemy AI uses the sword until its health drops below 50, I programmed my AI to use arrows for the first five rounds, dealing 10 damage to the enemy's health each time. Following this pattern, I switched to the sword on rounds six and seven, and fire for the rest.
Subsequently, I addressed the challenge of movement. To prevent the AI from accessing inaccessible cities, I developed a dictionary within the createCityDictionary function. This provided my AI with a comprehensive understanding of which cities it could access from each point on the map. However, I encountered an issue where my AI repeatedly moved to the same cities, squandering its resources. To resolve this, I sought the assistance of Chat GPT, who advised me to select a random city based on its accessibility and a calculated weight metric. Although this approach is not foolproof, it has enabled the AI to experience wins and losses.

Genetic Algorithm:

The second challenge that I encountered involved enhancing the realism of the game map by utilizing a genetic algorithm to adjust the position of cities. To accomplish this, I incorporated various metrics that enabled me to reward and penalize fitness based on specific city placements.
For instance, I imposed a penalty to fitness for city placement that was too close, too far, underwater, or located on mountains. Conversely, I rewarded city placement that adhered to the expected distance and elevation norms.
Additionally, I provided an incentive for city placement based on the shortest distance between two cities on the map. The longer this distance, the higher the fitness score that I attributed to the placement. This approach proved to be successful for the most part, although there are occasions where cities are still positioned too close together.

Text-To-Image Generation:

The third challenge that I aimed to tackle involved enhancing the entertainment value of the game's winning and losing scenarios. To accomplish this, I leveraged DALL-E from OpenAI to generate an image based on a text prompt that reflected the outcome of the game.
For instance, if the player emerged victorious and reached their destination, I displayed an image of them standing triumphantly. Conversely, if they met their demise in battle, I displayed an image of them being defeated. In the event that they ran out of funds, I displayed an image of an elf in tattered clothing and appearing emaciated.
While some might consider this approach to be rather grim, I found it to be a fascinating use of AI technology.



Additional Problems Solved

There were a couple non-ai issues that I had to solve. For example, there was a chance that a city would be isolated from the others with no connecting routes. I made a function called connectIsolatedCities that connected isolated cities to a random city in the list. 
The next problem I wanted to solve was making the destination city more interesting. I prompted chatGPT to make me a function to find the farthest city from the start given the dictionary of connected cities.
This is a dictionary in python.{0: [5], 1: [6, 9, 4, 2], 2: [9, 5, 1], 3: [], 4: [8, 1], 5: [9, 2, 0], 6: [9, 1], 7: [], 8: [4], 9: [6, 2, 5, 1]}
This is for a game. The player starts at city 0. From city 0, the player can travel to city 5. Write me some code to find the farthest city from the starting point that takes the most connections to get to.
This prompt gave me the getEndCity function which returns the farthest city from the start.

Appendix

AI Player Prompt:

reword this to sound better:

I have made it so an AI player can play this game. The two main challenges it needed to solve was figuring out where to go and how to win fights. Firstly, I worked on it's fighting ability. Since I already knew that the computer AI my AI would be fighting chose its decisions based on it's health, I used it to my advantage. Since I knew that the enemy AI would be using a sword until its health dropped below 50, I made my AI choose an arrow for the first 5 rounds knowing that it would do 10 damage to the enemy's health each time. Going off this pattern, I switched to the sword on rounds 6 and 7, and fire for the rest.
The next challenge I needed to work on was movement. In order to block the AI from going to inaccessible cities, I created a dictionary in a function called createCityDictionary. This allowed my AI to see which cities it could access from each city on the map. The next issue I had was trying to get it to stop moving to the same cities over and over, wasting its money. I was a little confused on the best/most fair way to do this, so I asked chat GPT to help. Chat GPT gave me a way to pick a random city based on its accessibility and a weight metric it calculated. it's not 100% effective, but the AI can both win and lose now.


Genetic Algorithm Prompt:

Reword what I say:

The second challenge was making the cities on the game map more realistically positioned using a genetic algorithm. I used several metrics to both punish and reward the city placement.
For example, I punished city placement that put cities too close, too far, under water, or on top of mountains.
I rewarded city placement when the distance and elevation was normal.
I also rewarded city placement. The longer the shortest distance between two cities on a map was, the more fitness I added. This seemed to work well for the most part. I do sometimes get cities too close


Text-to-Image Prompt:

Reword this:
The third problem I wanted to solve was making losing/winning more interesting. I utilized DALL-E from OpenAI to generate an image from a text prompt. This prompt was decided on the outcome of the game. If the player won and reached their destination, I showed them standing victorious. If they died in battle, I showed them defeated. If they ran out of money, I showed an elf dressed in rags and starving. It's a bit dark, but the AI technique was pretty cool.
