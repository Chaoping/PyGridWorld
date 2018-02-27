import GridWorldUI
import random
import numpy as np
from time import gmtime, strftime






class GridWorld():
    
    # World CONSTANTS 
    WORLD_SIZE_1 = 15
    WORLD_SIZE_2 = 15
    N_WATER_RESOURCE = 10
    N_FOOD_RESOURCE = 10
    RESOURCE_RELOCATE_RATE = 0.01 ## probability that a resource relocate. Setting to 0 disables relocation.
     
    
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
    VISUALIZE = False
    WRITE_TO_FILE = True
    DEBUG = False
    

    def __init__(self):
        # initialize simulator
        self.counter = 0
        self.current_mean_physiology = [0,0]
        self.alive_step = 0
        
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
        
        if self.WRITE_TO_FILE:
            self.file_handler = open("physiology"+"-"+strftime("%Y%m%d%H%M", gmtime())+".csv", "w")
            self.file_handler.write("Water,Food,Alive_step\n")
            
            

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


            # '''debug'''
            # print("temp water matrix")
            # print(augmented_water)
            # print("coordinates: ")
            # print(coordinates)

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

    def relocate_resources(self):
        for i in range(self.N_WATER_RESOURCE):
            if random.random() < self.RESOURCE_RELOCATE_RATE:
                self.water_matrix[self.water_coords[0][i], self.water_coords[1][i]] = 0
                while not self.water_matrix.sum() == self.N_WATER_RESOURCE:
                    self.water_matrix[random.randint(0,self.WORLD_SIZE_2-1),random.randint(0,self.WORLD_SIZE_1-1)] = 1

        for i in range(self.N_FOOD_RESOURCE):
            if random.random() < self.RESOURCE_RELOCATE_RATE:
                self.food_matrix[self.food_coords[0][i], self.food_coords[1][i]] = 0
                while not self.food_matrix.sum() == self.N_FOOD_RESOURCE:
                    self.food_matrix[random.randint(0,self.WORLD_SIZE_2-1),random.randint(0,self.WORLD_SIZE_1-1)] = 1
        


        self.water_coords = np.where(self.water_matrix == 1)
        self.food_coords = np.where(self.food_matrix == 1)

        
        


        


    # It takes an action input, caculate immedate reward,
    # generate new environment state and give part of the 
    # state information to the agent.
    def action(self, direction):
        # previous_index = self.agent_coord[0] * self.WORLD_SIZE_1 + self.agent_coord[1]
        
        # flag if the agent was on any resource before the move
        # if self.water_string[previous_index] == 1:
        #     water_to_relocate = True 
        # else:
        #     water_to_relocate = False

        # if self.food_string[previous_index] == 1:
        #     food_to_relocate = True 
        # else: 
        #     food_to_relocate = False

        #self.counter += 1
        #print ("step: " + str(self.counter))

        # move
        if direction[0]:
            if self.agent_coord[0] > 0:
                self.agent_coord[0] = self.agent_coord[0] - 1
                
        elif direction[1]:
            if self.agent_coord[1] > 0:
                self.agent_coord[1] = self.agent_coord[1] - 1
                
        elif direction[2]:
            if self.agent_coord[0] < self.WORLD_SIZE_2 - 1:
                self.agent_coord[0] = self.agent_coord[0] + 1
                
        elif direction[3]:
            if self.agent_coord[1] < self.WORLD_SIZE_1 - 1:
                self.agent_coord[1] = self.agent_coord[1] + 1
                
        elif direction[4]:
            pass





        # if direction[0]:
        #     if self.agent_coord[0] > 0:
        #         self.agent_coord[0] = self.agent_coord[0] - 1
        #         if water_to_relocate:
        #             self.water_string[previous_index] = 0
        #             while not sum(self.water_string) == self.N_WATER_RESOURCE:
        #                 self.water_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.water_coords = np.where(self.water_matrix == 1)
        #         if food_to_relocate:
        #             self.food_string[previous_index] = 0
        #             while not sum(self.food_string) == self.N_FOOD_RESOURCE:
        #                 self.food_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.food_coords = np.where(self.food_matrix == 1)
        # elif direction[1]:
        #     if self.agent_coord[1] > 0:
        #         self.agent_coord[1] = self.agent_coord[1] - 1
        #         if water_to_relocate:
        #             self.water_string[previous_index] = 0
        #             while not sum(self.water_string) == self.N_WATER_RESOURCE:
        #                 self.water_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.water_coords = np.where(self.water_matrix == 1)
        #         if food_to_relocate:
        #             self.food_string[previous_index] = 0
        #             while not sum(self.food_string) == self.N_FOOD_RESOURCE:
        #                 self.food_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.food_coords = np.where(self.food_matrix == 1)
        # elif direction[2]:
        #     if self.agent_coord[0] < self.WORLD_SIZE_2 - 1:
        #         self.agent_coord[0] = self.agent_coord[0] + 1
        #         if water_to_relocate:
        #             self.water_string[previous_index] = 0
        #             while not sum(self.water_string) == self.N_WATER_RESOURCE:
        #                 self.water_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.water_coords = np.where(self.water_matrix == 1)
        #         if food_to_relocate:
        #             self.food_string[previous_index] = 0
        #             while not sum(self.food_string) == self.N_FOOD_RESOURCE:
        #                 self.food_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.food_coords = np.where(self.food_matrix == 1)
        # elif direction[3]:
        #     if self.agent_coord[1] < self.WORLD_SIZE_1 - 1:
        #         self.agent_coord[1] = self.agent_coord[1] + 1
        #         if water_to_relocate:
        #             self.water_string[previous_index] = 0
        #             while not sum(self.water_string) == self.N_WATER_RESOURCE:
        #                 self.water_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.water_coords = np.where(self.water_matrix == 1)
        #         if food_to_relocate:
        #             self.food_string[previous_index] = 0
        #             while not sum(self.food_string) == self.N_FOOD_RESOURCE:
        #                 self.food_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.food_coords = np.where(self.food_matrix == 1)
        # elif direction[4]:
        #     if water_to_relocate and self.agent_water >= self.MAX_WATER:
        #         self.water_string[previous_index] = 0
        #         while not sum(self.water_string) == self.N_WATER_RESOURCE:
        #             self.water_string[random.randint(0,self.n_tiles - 1)] = 1
        #         self.water_coords = np.where(self.water_matrix == 1)
        #     if food_to_relocate and self.agent_food >= self.MAX_FOOD:
        #         self.food_string[previous_index] = 0
        #         while not sum(self.food_string) == self.N_FOOD_RESOURCE:
        #             self.food_string[random.randint(0,self.n_tiles - 1)] = 1
        #         self.food_coords = np.where(self.food_matrix == 1)


        
        # update to factor evaluation
        # if direction == 'w' or direction == 0:
        #     if self.agent_coord[0] > 0:
        #         self.agent_coord[0] = self.agent_coord[0] - 1
        #         if water_to_relocate:
        #             self.water_string[previous_index] = 0
        #             while not sum(self.water_string) == self.N_WATER_RESOURCE:
        #                 self.water_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.water_coords = np.where(self.water_matrix == 1)
        #         if food_to_relocate:
        #             self.food_string[previous_index] = 0
        #             while not sum(self.food_string) == self.N_FOOD_RESOURCE:
        #                 self.food_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.food_coords = np.where(self.food_matrix == 1)
        # elif direction == 'a' or direction == 1:
        #     if self.agent_coord[1] > 0:
        #         self.agent_coord[1] = self.agent_coord[1] - 1
        #         if water_to_relocate:
        #             self.water_string[previous_index] = 0
        #             while not sum(self.water_string) == self.N_WATER_RESOURCE:
        #                 self.water_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.water_coords = np.where(self.water_matrix == 1)
        #         if food_to_relocate:
        #             self.food_string[previous_index] = 0
        #             while not sum(self.food_string) == self.N_FOOD_RESOURCE:
        #                 self.food_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.food_coords = np.where(self.food_matrix == 1)
        # elif direction == 's' or direction == 2:
        #     if self.agent_coord[0] < self.WORLD_SIZE_2 - 1:
        #         self.agent_coord[0] = self.agent_coord[0] + 1
        #         if water_to_relocate:
        #             self.water_string[previous_index] = 0
        #             while not sum(self.water_string) == self.N_WATER_RESOURCE:
        #                 self.water_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.water_coords = np.where(self.water_matrix == 1)
        #         if food_to_relocate:
        #             self.food_string[previous_index] = 0
        #             while not sum(self.food_string) == self.N_FOOD_RESOURCE:
        #                 self.food_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.food_coords = np.where(self.food_matrix == 1)
        # elif direction == 'd' or direction == 3:
        #     if self.agent_coord[1] < self.WORLD_SIZE_1 - 1:
        #         self.agent_coord[1] = self.agent_coord[1] + 1
        #         if water_to_relocate:
        #             self.water_string[previous_index] = 0
        #             while not sum(self.water_string) == self.N_WATER_RESOURCE:
        #                 self.water_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.water_coords = np.where(self.water_matrix == 1)
        #         if food_to_relocate:
        #             self.food_string[previous_index] = 0
        #             while not sum(self.food_string) == self.N_FOOD_RESOURCE:
        #                 self.food_string[random.randint(0,self.n_tiles - 1)] = 1
        #             self.food_coords = np.where(self.food_matrix == 1)
        # elif direction == ' ' or direction == 4:


        # update physiology
        self.agent_water -= 1
        self.agent_food -= 1

        if self.water_matrix[self.agent_coord[0], self.agent_coord[1]] == 1:
            self.agent_water += self.REPLENISH_RATE

        if self.food_matrix[self.agent_coord[0], self.agent_coord[1]] == 1:
            self.agent_food += self.REPLENISH_RATE

        # limit the physiology in the range of [0, max]
        if self.agent_water < 0:
            self.agent_water = 0
        
        if self.agent_water > self.MAX_WATER:
            self.agent_water = self.MAX_WATER

        if self.agent_food < 0:
            self.agent_food = 0
        
        if self.agent_food > self.MAX_FOOD:
            self.agent_food = self.MAX_FOOD
        
        

        # self.world_dynamics()
        self.relocate_resources()
        
        # if random.random() < self.RESOURCE_RELOCATE_RATE:
        #     self.respawn_resources()



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

        # unroll everything
        state_representation = np.append(self.agent_water_view, self.agent_food_view)
        state_representation = np.append(state_representation, self.agent_land_view)
        state_representation = np.append(state_representation, self.agent_water / self.MAX_WATER) # normalize it
        state_representation = np.append(state_representation, self.agent_food / self.MAX_FOOD) #normalize it 


        if self.agent_food > 0 and self.agent_water>0:
            self.alive_step += 1
        self.counter += 1
        self.current_mean_physiology[0] += self.agent_water
        self.current_mean_physiology[1] += self.agent_food
        if self.counter == 2000:
            
            print("avg water over the last 2000 steps:")
            print(self.current_mean_physiology[0]/2000)
            print("avg food over the last 2000 steps:")
            print(self.current_mean_physiology[1]/2000)
            if self.WRITE_TO_FILE:
                self.file_handler.write(
                    str(self.current_mean_physiology[0]/2000)+
                    ","+str(self.current_mean_physiology[1]/2000)+","+
                    str(self.alive_step)+"\n")
            
            self.current_mean_physiology = [0,0]
            self.alive_step = 0
            self.counter = 0


        # if self.WRITE_TO_FILE:
        #     self.file_handler.write(str(self.agent_water)+","+str(self.agent_food)+"\n")


        
        return state_representation

    



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