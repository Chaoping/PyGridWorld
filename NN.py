import numpy as np
import math




class NeuralNetwork():
    
    ETA = 0.0001

    # A Neural Network    
    # An instance of the NN can be either created with 
    # new() method or load()

    def __init__(self):
        pass


    # structure is the number of units in each layer,
    # including the input layer but not the output layer
    # e.g, [3,5,2] indicates that the model takes input 
    # with 3 dimensions, and it has two hidden layers, with
    # 5 and 2 units respectively
    
    def new(self, structure):
        self.structure = structure
        
        # z = Wx + b is the linear combination
        
        # create containers for weights and weight gradients
        self.weights = []
        self.gradients = []
        np.random.seed(1)
                
        for i in range(len(structure)-1):
            self.weights.append(
                (np.random.rand(structure[i+1], structure[i] + 1) - 0.5) / 100
            )
            self.gradients.append(np.zeros(self.weights[i].shape))
 
        # weights for the output layer:
        self.final_weights = (np.random.rand(1, structure[-1] + 1) - 0.5) / 100
        self.final_gradients = np.zeros(self.final_weights.shape)

        # '''debug'''
        # for i in range(len(structure)-1):
        #     print("weights for hidden layer activation")
        #     print(self.weights[i])

        # print("weights for output layer")
        # print(self.final_weights)

    
    def tanh(self, z): # this simulation only uses thanh
        return (np.exp(z) - np.exp(-z)) / (np.exp(z) + np.exp(-z))

    
    def train(self, x, y):
        A = [] # a container to store all the activations
        A.append(x) # the 0th layer is actually the inputs

        A_gradients = [] # a container to store the gradients of the activations
        A_gradients.append(np.zeros(x.shape)) # the first item will not be used, just to align the two containers

        # feed forward
        for i in range(len(self.structure) - 1):
            A.append(
                self.tanh(np.dot(self.weights[i], np.concatenate((np.ones((1,1)),A[i])))) 
            )
            A_gradients.append(np.zeros(A[i+1].shape))


        y_predicted = np.dot(self.final_weights, np.concatenate((np.ones((1,1)),A[-1])))

        # back propagation 
        A_gradients[-1] = (y_predicted - y) * self.final_weights[:,1:].transpose()
        self.final_gradients = (y_predicted - y) * np.concatenate((np.ones((1,1)),A[-1])).transpose()
        self.final_weights = self.final_weights - self.final_gradients * self.ETA

        for i in range(-2, -(len(self.structure)+1), -1):
            temp = (1 - A[i+1]**2) * A_gradients[i+1]
            # print(temp)
            # print(A[i+1])
            
            # print("i="+str(i))
            # print(len(A_gradients))
            # print(A_gradients[-2])
            A_gradients[i] = np.dot(self.weights[i+1][:,1:].transpose(), temp) 
            self.gradients[i+1] = np.dot(temp,np.concatenate((np.ones((1,1)),A[i])).transpose())

            self.weights[i+1] = self.weights[i+1] - self.gradients[i+1] * self.ETA
 
        
        # '''debug'''
        # for i in range(len(self.structure)-1):
        #     print("Activations")
        #     print(A[i])

        # print("final linear result")
        # print(y_predicted)


      

    def predict(self,x):
        A = [] # a container to store all the activations
        A.append(x) # the 0th layer is actually the inputs

        


        # feed forward
        for i in range(len(self.structure) - 1):
            A.append(
                self.tanh(np.dot(self.weights[i], np.concatenate((np.ones((1,1)),A[i])))) 
            )

        # print("````")
        # print(np.dot(self.weights[0], np.concatenate((np.ones((1,1)),A[0]))))
        # print(self.tanh(np.dot(self.weights[0], np.concatenate((np.ones((1,1)),A[0])))))

        # print("????")
        # print(self.tanh(26.71298082))


        y_predicted = np.dot(self.final_weights, np.concatenate((np.ones((1,1)),A[-1])))
        return y_predicted



    def store(self):
        pass


    def load(self):
        pass




#test with a polynomial target function

def poly(x):
    a = np.array([1,2,3])
    
    y = 0
    for i in range(len(x)):
        y = y + a[i] * x[i] ** i
    y = y * 10
    return y


def test():
    nn_poly = NeuralNetwork()
    nn_poly.new([3,200,200])


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