import GridWorldUI
import random
import numpy as np




class GridWorld():
    
    # World CONSTANTS 
    WORLD_SIZE_1 = 4
    WORLD_SIZE_2 = 4
    N_WATER_RESOURCE = 2
    N_FOOD_RESOURCE = 2
    RESOURCE_RELOCATE_RATE = 0.001 ## probability that a resource relocate. Setting to 0 disables relocation.
     
    
    # Agent CONSTANTS
    INITIAL_X1 = -1 # Spawning coordinates. Setting to -1 to spawn at random.
    INITIAL_X2 = -1
    MAX_WATER = 30
    INITIAL_WATER = 20
    MAX_FOOD = 30
    INITIAL_FOOD = 20
    DECAY_RATE = 1
    REPLENISH_RATE = 5

    # SIMULATION CONSTANTS
    VISUALIZE = True
    
    



    def __init__(self):
        # initialize agent
        self.agent_coord = [self.INITIAL_X1,self.INITIAL_X2]
        if self.agent_coord[0] == -1:
            self.agent_coord[0] = random.randint(0, self.WORLD_SIZE_1 - 1)
        if self.agent_coord[1] == -1:
            self.agent_coord[1] = random.randint(0, self.WORLD_SIZE_2 - 1)
        self.agent_water = float(self.INITIAL_WATER)
        self.agent_food = float(self.INITIAL_FOOD)

        # initialize world
        # note: multiple instances of same type of resource may spawn at the same position.         
        self.water_matrix = np.zeros((self.WORLD_SIZE_2, self.WORLD_SIZE_1))    
        self.water_matrix[ ## spawn water
            np.random.choice(range(self.WORLD_SIZE_2),self.N_WATER_RESOURCE),
            np.random.choice(range(self.WORLD_SIZE_1),self.N_WATER_RESOURCE)
            ] = 1
        self.food_matrix = np.zeros((self.WORLD_SIZE_2, self.WORLD_SIZE_1))
        self.food_matrix[ ## spawn food
            np.random.choice(range(self.WORLD_SIZE_2),self.N_FOOD_RESOURCE),
            np.random.choice(range(self.WORLD_SIZE_1),self.N_FOOD_RESOURCE)
            ] = 1
        

        # Visualize
        if self.VISUALIZE:
            ui = GridWorldUI.GridWorldUI(self.WORLD_SIZE_1,self.WORLD_SIZE_2)


    def test(self):
        print(self.water_matrix)
        print(self.food_matrix)


    # It takes an action input, caculate immedate reward,
    # generate new environment state and give part of the 
    # state information to the agent.
    def action(self):
        return ()



a = GridWorld()
input()
a.test()