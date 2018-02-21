import GridWorldUI
import random
import numpy as np





class GridWorld():
    
    # World CONSTANTS 
    WORLD_SIZE_1 = 20
    WORLD_SIZE_2 = 20
    N_WATER_RESOURCE = 2
    N_FOOD_RESOURCE = 2
    RESOURCE_RELOCATE_RATE = 0.0 ## probability that a resource relocate. Setting to 0 disables relocation.
     
    
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
    DEBUG = True

    def __init__(self):
        # initialize simulator
        self.counter = 0
        
        # initialize world
        self.n_tiles = self.WORLD_SIZE_1 * self.WORLD_SIZE_2
        self.respawn_resources()

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
            self.ui = GridWorldUI.GridWorldUI(
                self.WORLD_SIZE_1,
                self.WORLD_SIZE_2, 
                self.agent_coord[0], 
                self.agent_coord[1],
                self.AGENT_SIGHT             
                )
            self.ui.update_water(self.water_coords[0], self.water_coords[1])
            self.ui.update_food(self.food_coords[0], self.food_coords[1])
            self.ui.update_agent_view(self.agent_land_view,self.agent_water_view,self.agent_food_view)
            
            

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
                coordinates[0]:coordinates[1]+1,
                coordinates[2]:coordinates[3]+1
            ]
            self.agent_food_view = self.food_matrix[
                coordinates[0]:coordinates[1]+1,
                coordinates[2]:coordinates[3]+1
            ]

        
        else: # construct a bigger matrix to corp from
            augmented_water = np.zeros((
                self.WORLD_SIZE_2 + 2 * self.AGENT_SIGHT, 
                self.WORLD_SIZE_1 + 2 * self.AGENT_SIGHT))
            
            # water
            augmented_water[
                self.AGENT_SIGHT:self.WORLD_SIZE_2 + self.AGENT_SIGHT,
                self.AGENT_SIGHT:self.WORLD_SIZE_1 + self.AGENT_SIGHT,
                ] = self.water_matrix


            '''debug'''
            print("temp water matrix")
            print(augmented_water)
            print("coordinates: ")
            print(coordinates)

            self.agent_water_view = augmented_water[
                (coordinates[0] + self.AGENT_SIGHT) :(coordinates[1] + self.AGENT_SIGHT + 1),
                (coordinates[2] + self.AGENT_SIGHT) :(coordinates[3] + self.AGENT_SIGHT + 1)
            ]


            # food
            augmented_food = np.zeros((
                self.WORLD_SIZE_2 + 2 * self.AGENT_SIGHT, 
                self.WORLD_SIZE_1 + 2 * self.AGENT_SIGHT))

            augmented_food[
                self.AGENT_SIGHT:self.WORLD_SIZE_2 + self.AGENT_SIGHT,
                self.AGENT_SIGHT:self.WORLD_SIZE_1 + self.AGENT_SIGHT,
                ] = self.food_matrix

            self.agent_food_view = augmented_food[
                coordinates[0] + self.AGENT_SIGHT :coordinates[1] + self.AGENT_SIGHT + 1,
                coordinates[2] + self.AGENT_SIGHT :coordinates[3] + self.AGENT_SIGHT + 1
            ]



            
    def respawn_resources(self):
        
        # the following code is discarded because multiple resources of the same
        # type may respawn at the same location

        # self.water_coords = (
        #     np.random.choice(range(self.WORLD_SIZE_2),self.N_WATER_RESOURCE),
        #     np.random.choice(range(self.WORLD_SIZE_1),self.N_WATER_RESOURCE)
        # )
        # self.food_coords = (
        #     np.random.choice(range(self.WORLD_SIZE_2),self.N_WATER_RESOURCE),
        #     np.random.choice(range(self.WORLD_SIZE_1),self.N_WATER_RESOURCE)
        # )       
        # 
        # self.water_matrix = np.zeros((self.WORLD_SIZE_2, self.WORLD_SIZE_1))    
        # self.water_matrix[ ## spawn water
        #     self.water_coords[0], self.water_coords[1]
        #     ] = 1
        # self.food_matrix = np.zeros((self.WORLD_SIZE_2, self.WORLD_SIZE_1))
        # self.food_matrix[ ## spawn food
        #     self.food_coords[0], self.food_coords[1]
        #     ] = 1 

        
        
        self.water_string = np.zeros(self.n_tiles)
        self.water_string[random.sample(range(self.n_tiles),self.N_WATER_RESOURCE)] = 1
        self.water_matrix = self.water_string.reshape((self.WORLD_SIZE_2, self.WORLD_SIZE_1))
        self.water_coords = np.where(self.water_matrix == 1)

        self.food_string  = np.zeros(self.n_tiles)
        self.food_string[random.sample(range(self.n_tiles),self.N_FOOD_RESOURCE)] = 1
        self.food_matrix = self.food_string.reshape((self.WORLD_SIZE_2, self.WORLD_SIZE_1))
        self.food_coords = np.where(self.food_matrix == 1)

    #def relocate_resource(self):
        
        
        


        


    # It takes an action input, caculate immedate reward,
    # generate new environment state and give part of the 
    # state information to the agent.
    def action(self, direction):
        previous_index = self.agent_coord[0] * self.WORLD_SIZE_1 + self.agent_coord[1]
        
        # flag if the agent was on any resource before the move
        if self.water_string[previous_index] == 1:
            water_to_relocate = True 
        else:
            water_to_relocate = False

        if self.food_string[previous_index] == 1:
            food_to_relocate = True 
        else: 
            food_to_relocate = False

        self.counter += 1
        print ("step: " + str(self.counter))

        # move
        if direction == 'w':
            if self.agent_coord[0] > 0:
                self.agent_coord[0] = self.agent_coord[0] - 1
                if water_to_relocate:
                    self.water_string[previous_index] = 0
                    while not sum(self.water_string) == self.N_WATER_RESOURCE:
                        self.water_string[random.randint(0,self.n_tiles - 1)] = 1
                    self.water_coords = np.where(self.water_matrix == 1)
                if food_to_relocate:
                    self.food_string[previous_index] = 0
                    while not sum(self.food_string) == self.N_FOOD_RESOURCE:
                        self.food_string[random.randint(0,self.n_tiles - 1)] = 1
                    self.food_coords = np.where(self.food_matrix == 1)
        elif direction == 'a':
            if self.agent_coord[1] > 0:
                self.agent_coord[1] = self.agent_coord[1] - 1
                if water_to_relocate:
                    self.water_string[previous_index] = 0
                    while not sum(self.water_string) == self.N_WATER_RESOURCE:
                        self.water_string[random.randint(0,self.n_tiles - 1)] = 1
                    self.water_coords = np.where(self.water_matrix == 1)
                if food_to_relocate:
                    self.food_string[previous_index] = 0
                    while not sum(self.food_string) == self.N_FOOD_RESOURCE:
                        self.food_string[random.randint(0,self.n_tiles - 1)] = 1
                    self.food_coords = np.where(self.food_matrix == 1)
        elif direction == 's':
            if self.agent_coord[0] < self.WORLD_SIZE_2 - 1:
                self.agent_coord[0] = self.agent_coord[0] + 1
                if water_to_relocate:
                    self.water_string[previous_index] = 0
                    while not sum(self.water_string) == self.N_WATER_RESOURCE:
                        self.water_string[random.randint(0,self.n_tiles - 1)] = 1
                    self.water_coords = np.where(self.water_matrix == 1)
                if food_to_relocate:
                    self.food_string[previous_index] = 0
                    while not sum(self.food_string) == self.N_FOOD_RESOURCE:
                        self.food_string[random.randint(0,self.n_tiles - 1)] = 1
                    self.food_coords = np.where(self.food_matrix == 1)
        elif direction == 'd':
            if self.agent_coord[1] < self.WORLD_SIZE_1 - 1:
                self.agent_coord[1] = self.agent_coord[1] + 1
                if water_to_relocate:
                    self.water_string[previous_index] = 0
                    while not sum(self.water_string) == self.N_WATER_RESOURCE:
                        self.water_string[random.randint(0,self.n_tiles - 1)] = 1
                    self.water_coords = np.where(self.water_matrix == 1)
                if food_to_relocate:
                    self.food_string[previous_index] = 0
                    while not sum(self.food_string) == self.N_FOOD_RESOURCE:
                        self.food_string[random.randint(0,self.n_tiles - 1)] = 1
                    self.food_coords = np.where(self.food_matrix == 1)
        elif direction == ' ':
            pass

        # update physiology
        self.agent_water -= 1
        self.agent_food -= 1

        if self.water_matrix[self.agent_coord[0], self.agent_coord[1]] == 1:
            self.agent_water += self.REPLENISH_RATE

        if self.food_matrix[self.agent_coord[0], self.agent_coord[1]] == 1:
            self.agent_food += self.REPLENISH_RATE
        
        

        # self.world_dynamics()
        if random.random() < self.RESOURCE_RELOCATE_RATE:
            self.respawn_resources()



        # update agent view for next decision
        self.update_view()

        


        if self.VISUALIZE:
            self.ui.move_agent(self.agent_coord[0],self.agent_coord[1])
            self.ui.update_water(self.water_coords[0], self.water_coords[1])
            self.ui.update_food(self.food_coords[0], self.food_coords[1])

            self.ui.update_agent_view(self.agent_land_view, self.agent_water_view, self.agent_food_view)
            self.ui.update_physiology(self.agent_water,self.MAX_WATER, self.agent_food, self.MAX_FOOD)
            

        if self.DEBUG:            
            # print("coordinates:")
            # print(self.agent_coord)
            
            # print("water map:")
            # print(self.water_matrix)
            print("agent sees water:")
            print(self.agent_water_view)


            print("agent sees food")
            print(self.agent_food_view)

            # print("agent sees map")
            # print(self.agent_land_view)

            # print("water: "+ str(self.agent_water))
            # print("food: "+ str(self.agent_food))

        
        return ()





    def test(self):
        print(self.water_matrix)
        print(self.food_matrix)
        print(self.agent_coord)
        print(self.agent_land_view)

        print("water matrix and agent water view")
        print(self.water_matrix)
        print(self.agent_water_view)

        

'''
a = GridWorld()
input("model created. waiting for command")
a.test()
input()
'''