import copy
import multiprocessing
from random import randint
from joblib import Parallel, delayed

class GeneticAlgorithm:
    def __init__(self, networks=None, networks_shape=None, population_size=1000, generation_number=100,
                 crossover_rate=0.3, crossover_method='neuron', mutation_rate=0.7, mutation_method='weight'):
        self.networks_shape = networks_shape
        if self.networks_shape is None:  # if no shape is provided
            self.networks_shape = [21, 16, 3]  # default shape
        self.networks = networks

        if networks is None:  # if no networks are provided
            self.networks = []
            for i in range(population_size):  # producing population
                self.networks.append(NeuralNetwork(self.networks_shape))

        self.population_size = population_size
        self.generation_number = generation_number
        self.crossover_rate = crossover_rate
        self.crossover_method = crossover_method
        self.mutation_rate = mutation_rate
        self.mutation_method = mutation_method