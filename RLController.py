from NN import NeuralNetwork
import GridWorld
import numpy as np
from collections import deque 
import random
from time import sleep
import copy

class RL():
    # 25 water sight, 25 food sight, 25 land sight
    # previous 2 turns' actions: 2 * 5
    # 2 physiologies
    
    GAMMA = 0.5
    STATE_FEATURES = 25 + 25 + 25 + 2 * 5 + 2
    ACTIONS = 5
    INPUT_DIM = STATE_FEATURES + ACTIONS
    NN_STRUCTURE = [INPUT_DIM, 4,4,4]
    SWITCH_AT = 2000
    ACTION_FACTORS = [[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]]


    def __init__(self):
        self.gw = GridWorld.GridWorld()
        self.nets = []
        
        # create two N-NETS for fixed Q-targets switches
        self.nets.append(NeuralNetwork())
        self.nets.append(NeuralNetwork())
        self.nets[0].new(self.NN_STRUCTURE)
        self.nets[1].new(self.NN_STRUCTURE)
        self.cache_index = 0
        self.active_index = 1

        # epsilon to modify the greediness
        self.epsilon = 1
        # epsilon := 1/k
        self.k = 1

        # initialize starting situations
        self.state = self.gw.action(self.ACTION_FACTORS[4])
        self.previous_actions = deque([0,0,0,0,1,0,0,0,0,1]) #assume it has not moved for two steps before the start.
        self.water_remembered = self.state[-1]
        self.food_remembered = self.state[-2]

    def run(self):

        while True:
            transitions = []
            
            # remember a list of transitions for experience replay
            # train on the transitions after a 
            # fixed number of steps

            for step in range(self.SWITCH_AT):
                current_transition = []
                # Each transition has several parts
                # plug in supervised learning:
                # input consists the state and the action
                # output is the immediate reward plus the greedy reward

                features = np.concatenate((
                    self.state,
                    self.previous_actions
                ))

                
                
                
                # pick an action
                # epsilon probability to pick at random
                # 1 - epsilon probability to pick greedy
                if random.random() < self.epsilon:
                    self.action = self.ACTION_FACTORS[random.randint(0,4)]
                else:
                    
                    # pick a greedy action
                    Q = []
                    for i in range(5):                         
                        # concatenate features and action
                        self.decision_factor = np.append(features, self.ACTION_FACTORS[i])
                        Q.append(
                            # compare the Q
                            self.nets[self.cache_index].predict(                           
                                self.decision_factor.reshape(self.INPUT_DIM,1)))
                        

                    self.action = self.ACTION_FACTORS[Q.index(max(Q))]

                # store decision factor (combination of states and action)
                current_transition.append(
                    np.append(features, self.action).reshape(self.INPUT_DIM,1)
                )
                
                # take action
                self.state = self.gw.action(self.action)

                # immediate reward
                if self.state[-1] >= 0 and self.state[-2] >= 0:
                    self.reward = 5
                elif self.state[-1] >= self.water_remembered or self.state[-2] >= self.food_remembered:
                    self.reward = 0
                else:
                    self.reward = -1
                
                self.water_remembered = self.state[-1]
                self.food_remembered = self.state[-2]

                # update previous actions
                for i in range(5):
                    self.previous_actions.popleft()
                    self.previous_actions.append(self.action[i])

                # what is the value of s'?
                features = np.concatenate((
                    self.state,
                    self.previous_actions
                ))

                Q = []
                for i in range(5):                         
                    # concatenate features and action
                    self.decision_factor = np.append(features, self.ACTION_FACTORS[i])
                    #print(self.decision_factor)

                    Q.append(
                        # compare the Q
                        self.nets[self.cache_index].predict(                           
                            self.decision_factor.reshape(self.INPUT_DIM,1)))
                    #print("Q_"+str(i)+" = "+str(Q[i]))
                s_prime_value = max(Q)
                predicted_value = self.reward + s_prime_value * self.GAMMA
                #input("go")
                #sleep(0.01)
                print("target = " + str(predicted_value))
                
                current_transition.append(predicted_value)
                self.nets[self.active_index].train(current_transition[0], current_transition[1])
                print("respon = " + str(self.nets[self.active_index].predict(current_transition[0])))

                transitions.append(current_transition)
                
            self.k += 1

            #print(self.epsilon)
            # train again using experience replay
            shuffle = random.sample(range(self.SWITCH_AT), self.SWITCH_AT)
            
            print(len(transitions))

            for i in shuffle:
                self.nets[self.active_index].train(transitions[i][0],transitions[i][1])
                #print("replaying....")

            # update cache
            self.nets[self.cache_index] = copy.deepcopy(self.nets[self.active_index])
            
            
            


    # evaluate an action given s. 
    # it only uses the cached weights
    def Q(self,s,a):
        x = np.concatenate((s,a)).reshape(self.INPUT_DIM,1)
        return self.nets[self.cache_index].predict(x)


    

        


rl = RL()
rl.run()
        