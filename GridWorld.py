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
    AGENT_SIGHT = 2

    # SIMULATION CONSTANTS
    VISUALIZE = True

    def __init__(self):
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

        # initialize agent
        self.agent_coord = [self.INITIAL_X1,self.INITIAL_X2]
        if self.agent_coord[0] == -1:
            self.agent_coord[0] = random.randint(0, self.WORLD_SIZE_1 - 1)
        if self.agent_coord[1] == -1:
            self.agent_coord[1] = random.randint(0, self.WORLD_SIZE_2 - 1)

        self.agent_water = self.INITIAL_WATER
        self.agent_food = self.INITIAL_FOOD
        self.agent_sight_dimension = (self.AGENT_SIGHT * 2 + 1, self.AGENT_SIGHT * 2 + 1)   
        
        self.update_view()
         
        # Visualize
        if self.VISUALIZE:
            ui = GridWorldUI.GridWorldUI(self.WORLD_SIZE_1,self.WORLD_SIZE_2)

    def update_view(self):
        coordinates = (
            self.agent_coord[0]-self.AGENT_SIGHT,
            self.agent_coord[0]+self.AGENT_SIGHT,
            self.agent_coord[1]-self.AGENT_SIGHT,
            self.agent_coord[1]+self.AGENT_SIGHT,
            )
        
        # update land view. (1 for inaccessible tiles)
        self.agent_land_view = np.zeros(self.agent_sight_dimension)
        if self.agent_coord[0] - self.AGENT_SIGHT < 0: 
            self.agent_land_view[0: self.AGENT_SIGHT - self.agent_coord[0],:] = 1
        if self.agent_coord[1] - self.AGENT_SIGHT < 0: 
            self.agent_land_view[:, 0: self.AGENT_SIGHT - self.agent_coord[1]] = 1
        
        if self.agent_coord[0] + self.AGENT_SIGHT > self.WORLD_SIZE_2 - 1:
            self.agent_land_view[(self.WORLD_SIZE_2 - self.agent_coord[0] - self.AGENT_SIGHT - 1):,:] = 1
        if self.agent_coord[1] + self.AGENT_SIGHT > self.WORLD_SIZE_1 - 1:
            self.agent_land_view[:,(self.WORLD_SIZE_1 - self.agent_coord[1] - self.AGENT_SIGHT - 1):] = 1

        # update water and food
        self.agent_water_view = np.zeros(self.agent_sight_dimension)

        # if the agent is far away from an edge of the map
        if (coordinates[0] >= 0 and
            coordinates[1] < self.WORLD_SIZE_2 and
            coordinates[2] >= 0 and
            coordinates[3] < self.WORLD_SIZE_1):

            self.agent_water_view = self.water_matrix[
                coordinates[0]:coordinates[1],
                coordinates[2]+1:coordinates[3]+1
            ]
            self.agent_food_view = self.food_matrix[
                coordinates[0]:coordinates[1],
                coordinates[2]+1:coordinates[3]+1
            ]

        
        else: # construct a bigger matrix to corp from
            augmented_matrix = np.zeros((
                self.WORLD_SIZE_2 + 2 * self.AGENT_SIGHT, 
                self.WORLD_SIZE_1 + 2 * self.AGENT_SIGHT))
            
            # water
            augmented_matrix[
                self.AGENT_SIGHT:self.WORLD_SIZE_2 + self.AGENT_SIGHT,
                self.AGENT_SIGHT:self.WORLD_SIZE_1 + self.AGENT_SIGHT,
                ] = self.water_matrix


            '''debug'''
            print("temp water matrix")
            print(augmented_matrix)
            

            self.agent_water_view = augmented_matrix[
                coordinates[0] + self.AGENT_SIGHT :coordinates[1] + self.AGENT_SIGHT + 1,
                coordinates[2] + self.AGENT_SIGHT :coordinates[3] + self.AGENT_SIGHT + 1
            ]


            # food
            augmented_matrix[
                self.AGENT_SIGHT:self.WORLD_SIZE_2 + self.AGENT_SIGHT,
                self.AGENT_SIGHT:self.WORLD_SIZE_1 + self.AGENT_SIGHT,
                ] = self.food_matrix

            self.agent_food_view = augmented_matrix[
                coordinates[0] + self.AGENT_SIGHT :coordinates[1] + self.AGENT_SIGHT + 1,
                coordinates[2] + self.AGENT_SIGHT :coordinates[3] + self.AGENT_SIGHT + 1
            ]



            


        


    # It takes an action input, caculate immedate reward,
    # generate new environment state and give part of the 
    # state information to the agent.
    def action(self, direction):
        

        
        return ()





    def test(self):
        print(self.water_matrix)
        print(self.food_matrix)
        print(self.agent_coord)
        print(self.agent_land_view)

        print("water matrix and agent water view")
        print(self.water_matrix)
        print(self.agent_water_view)


a = GridWorld()
input()
a.test()
input()