import numpy as np
import math

LEAKY_COEFICIENT = 0.01




class NNReLU():
    
    # learning rate
    ETA = 0.01

    def __init__(self, structure = None, load = False, weights = None):
        # initialize a new NNReLU class
        if not load:
            self.structure = structure
            # create containers for weights and weight gradients
            self.weights = []
            self.gradients = []
            np.random.seed(1)
                    
            for i in range(len(structure)-1):
                self.weights.append(
                    np.random.rand(structure[i+1], structure[i] + 1) /50 
                )
                self.gradients.append(np.zeros(self.weights[i].shape))
    
            # weights for the output layer:
            self.final_weights = (np.random.rand(1, structure[-1] + 1)-0.5) / 50
            self.final_gradients = np.zeros(self.final_weights.shape)

            # self.report_count = 0
            
        else:
            #load
            pass

    def leakyReLU(self,z):
        a = z.copy()
        
        # if self.report_count == 10000:
        #     print(z)
            

        

        a[np.where(z<0)] = z[np.where(z<0)] * LEAKY_COEFICIENT
        return a



    def train(self, x, y):
        A = [] # a container to store all the activations
        A.append(x) # the 0th layer is actually the inputs

        A_gradients = [] # a container to store the gradients of the activations
        A_gradients.append(np.zeros(x.shape)) # the first item will not be used, just to align the two containers

        # feed forward
        for i in range(len(self.structure) - 1):
            A.append(
                self.leakyReLU(np.dot(self.weights[i], np.concatenate((np.ones((1,1)),A[i])))) 
            )
            A_gradients.append(np.zeros(A[i+1].shape))

        y_predicted = np.dot(self.final_weights, np.concatenate((np.ones((1,1)),A[-1])))

        # back propagation 
        A_gradients[-1] = (y_predicted - y) * self.final_weights[:,1:].transpose()
        self.final_gradients = (y_predicted - y) * np.concatenate((np.ones((1,1)),A[-1])).transpose()

        for i in range(-2, -(len(self.structure)+1), -1):
            #temp = (1 - A[i+1]**2) * A_gradients[i+1]
            
            # f'(x) = 1 if f(x) > 0 else f'(x) = LEAKY_COEFICIENT
            temp =  A_gradients[i+1]
            
            '''debug'''
            #print(temp[np.where(A[i+1]<0)])
            #print(A_gradients[i+1][np.where(A[i+1]<0)])
            #input()
            
            if len(np.where(A[i+1]<0)) > 0:
                temp[np.where(A[i+1]<0)] = LEAKY_COEFICIENT * A_gradients[i+1][np.where(A[i+1]<0)]

            


            A_gradients[i] = np.dot(self.weights[i+1][:,1:].transpose(), temp) 
            self.gradients[i+1] = np.dot(temp,np.concatenate((np.ones((1,1)),A[i])).transpose())

            self.weights[i+1] = self.weights[i+1] - self.gradients[i+1] * self.ETA


        '''debug'''
        # self.report_count += 1
        # if (self.report_count > 10000):
        #     self.report_count = 0



    def predict(self,x):
        A = [] # a container to store all the activations
        A.append(x) # the 0th layer is actually the inputs

        


        # feed forward
        for i in range(len(self.structure) - 1):
            A.append(
                self.leakyReLU(np.dot(self.weights[i], np.concatenate((np.ones((1,1)),A[i])))) 
            )

        # print("````")
        # print(np.dot(self.weights[0], np.concatenate((np.ones((1,1)),A[0]))))
        # print(self.tanh(np.dot(self.weights[0], np.concatenate((np.ones((1,1)),A[0])))))

        # print("????")
        # print(self.tanh(26.71298082))


        y_predicted = np.dot(self.final_weights, np.concatenate((np.ones((1,1)),A[-1])))
        return y_predicted

def poly(x):
    a = np.array([1,2,3])
    
    y = 0
    for i in range(len(x)):
        y = y + a[i] * x[i] ** i
    y = y * 10
    return y


def test():
    nn_poly = NNReLU([3,100,100,100])


    for j in range(100):
        for i in range(20000):
            x = (np.random.rand(3,1) - 0.5) * 2
            y = poly(x)
            nn_poly.train(x,y)
            
        x = (np.random.rand(3,1) - 0.5) * 2
        y = poly(x)
        ybar = nn_poly.predict(x)[0,0]

        print("y = " + str(y[0]))
        print("y^= "+ str(ybar))
        print("e = " + str((y[0] - ybar)**2))
        print()

#test()


