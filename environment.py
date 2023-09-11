from typing import Callable
import random
from PIL import Image

from individual import Individual

class HyperParameters:
    def __init__(
        self,
        fitness_function: Callable[[Image.Image, Individual], float],
        cap_population_size: int=50
    ):
        self.fitness_function = fitness_function
        self.cap_population_size = cap_population_size

class Generation:
    def __init__(self,
                 gen_number: int,
                 population: list[Individual]=[]) -> None:
        self.population = population
        self.gen_number = gen_number
    
    def get_top_individuals(self, quantity: int) -> list[Individual]:
        self.population.sort(reverse=True)
        return self.population[:quantity]
    
    def set_population(self, population: list[Individual]) -> None:
        self.population = population
    
    def get_population(self) -> list[Individual]:
        return self.population

class Environment:
    def __init__(self,
                 objective: Image.Image,
                 hyper_parameters: HyperParameters
    ) -> None:
        self.current_generation = Generation(0)

        self.cap_population_size = hyper_parameters.cap_population_size
        self.fitness_function = hyper_parameters.fitness_function
        self.objective = objective

        initial_population = self.generate_initial_population()
        self.current_generation.set_population(initial_population)
    
    def generate_initial_population(self) -> list[Individual]:
        population: list[Individual] = []
        for _ in range(self.cap_population_size):
            figure_quantity = random.randint(1, 5)
            individual = Individual(figure_quantity)
            individual.randomize_figures()

            population.append(individual)

        return population
    
    def calculate_fitness(self) -> None:
        for individual in self.current_generation.get_population():
            individual_fitness: float =\
                self.fitness_function(self.objective, individual)
            individual.set_fitness_value(individual_fitness)

    def get_top_individuals(self, quantity: int) -> list[Individual]:
        return self.current_generation.get_top_individuals(quantity)
    
    def get_current_population(self) -> list[Individual]:
        return self.current_generation.get_population()
