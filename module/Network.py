import numpy as np
import pygame
#import Game
import math
import time
from pygame import gfxdraw

#shape = (56,16,8,4) # 57x12, 17x8, 9x4
numLayer = 4

def sigmoid(z):
    """
    The sigmoid function, classic neural net activation function
    @jit is used to speed up computation
    """
    return 1.0 / (1.0 + np.exp(-z))

class NeuralNetwork:
    def __init__(self, network_shape):
        #self.shape = shape
        self.weights = []
        self.biases = []
        self.score = 0
        weightShape = []
        for i in range(len(network_shape)-1):
            weightShape.append([network_shape[i],network_shape[i+1]])
        #weightShape = [[shape[0],shape[1]],[shape[1], shape[2]],[shape[2], shape[3]]]
        for i in range(numLayer-1):
            self.weights.append(np.random.randn(weightShape[i][0],weightShape[i][1]))
        for i in range(numLayer - 1):
            self.biases.append(np.random.randn(1,weightShape[i][1]))

    def forward(self, input):
        for b, w in zip(self.biases, self.weights):
            #print(str(w.size/w[0].size) + ' ' + str(w[0].size))
            #print(b.size)
            #print(str(input.size/input[0].size) + ' ' + str(input[0].size))
            input = sigmoid(np.dot(input, w) + b)
        #print(input)
        return input.ravel()

    def save(self):
        np.save('E:/Tai_lieu/ReinforcementLearningProject/Snake/saved_weights', self.weights)
        np.save('E:/Tai_lieu/ReinforcementLearningProject/Snake/saved_biases', self.biases)

    def load(self):
        self.weights = np.load('E:/Tai_lieu/ReinforcementLearningProject/Snake/saved_weights')
        self.biases = np.load('E:/Tai_lieu/ReinforcementLearningProject/Snake/saved_biases')

    def filterOutput(self, output):
        maxVal = np.max(output)

        for i in range(output.size):
            if maxVal == output[i]:
                output[i] = 1
            else:
                output[i] = 0
        return output

    def render(self, window, vision, startPos):
        neuralRadius = 5
        neuralRadiusFirstLayer = 3
        lineWidth = 2
        marginNeuralFirstLayer = 5
        marginNeural = 20
        marginLayer = 150
        """
                Display the network at the current state in the right part of game window
                The function supports any network shape but is not very flexible
                I plan to work on it for later projects
                :param window: surface, game window
                :param vision: column of int, snake vision needed to show inputs
                """
        network = [np.array(vision)]  # will contain all neuron activation from each layer
        for i in range(len(self.biases)):
            activation = sigmoid(np.dot(network[i], self.weights[i]) + self.biases[i])  # compute neurons activations
            network.append(activation)  # append it
        network[len(self.biases)][0] = self.filterOutput(network[len(self.biases)][0])

        for i in range(len(network)):  # for each layer
            startPosLayerX = startPos[0] + i*marginLayer
            if i == 0:
                startPosLayerY = startPos[1] - math.floor(len(network[i][0])/2) * (marginNeuralFirstLayer + neuralRadiusFirstLayer * 2)
                currentNeuralRadius = neuralRadiusFirstLayer
            else:
                startPosLayerY = startPos[1] - math.floor(len(network[i][0])/2) * (marginNeural + neuralRadius * 2)
                currentNeuralRadius = neuralRadius
            for j in range(len(network[i][0])):  # for each neuron in current layer
                x = startPosLayerX
                if i == 0:
                    y = startPosLayerY + j*(marginNeuralFirstLayer + neuralRadiusFirstLayer * 2)
                else:
                    y = startPosLayerY + j*(marginNeural + neuralRadius * 2)
                intensity = abs(int(network[i][0][j] * 255))  # neuron intensity
                if intensity > 255:
                    intensity = 255
                elif intensity < 0:
                    intensity = 0

                if i < len(network) - 1:
                    for k in range(len(network[i + 1][0])):  # connections
                        x2 = startPos[0] + (i + 1) * marginLayer
                        y2 = startPos[1] - math.floor(len(network[i+1][0])/2) * (marginNeural + neuralRadius * 2) + k * (marginNeural + neuralRadius * 2)
                        intensityL = (intensity/2) + 60
                        if intensityL < 100:
                            intensityL = 0
                        pygame.gfxdraw.line(window, x, y, x2, y2,  # draw connection
                                            (0, intensityL, intensityL, 90))

                pygame.gfxdraw.filled_circle(window, x, y, currentNeuralRadius, (intensity, 0, 0))  # draw neuron
                pygame.gfxdraw.aacircle(window, x, y, currentNeuralRadius, (255, 255, 255))
        pygame.display.update()
"""
pygame.init()
dis = pygame.display.set_mode((800,600))
isRun = True
while isRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRun = False
    #example = np.random.randn(1,56)
    #example= np.random.randint(2,size = (1,56))
    example = np.random.choice(2,size = (1,56), p = [0.95,0.05])
    #vision = example.ravel()
    n = NeuralNetwork()
    n.render(dis,example,[50,300])
    time.sleep(0.07)
"""