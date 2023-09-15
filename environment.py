from typing import Callable, Union
import random
import math
from PIL import Image
from dataclasses import dataclass

from individual import Individual

@dataclass
class HyperParameters:
    fitness_function: Callable[[Image.Image, Image.Image], float]
    crossover_function: Callable[[Individual, Individual], Individual]
    cap_population_size: int = 50
    top_individuals_percentage: float = 0.1
    mutation_probability: float = 0.1
    mutation_quantity: float = 0.1
    max_gen:int = 100

class Generation:
    def __init__(self,
                 gen_number: int,
                 population: list[Individual]=[]) -> None:
        print(f"Created population {gen_number}")
        self.population = population
        self.gen_number = gen_number

        self.sorted:bool = False

    def get_top_individuals(self, quantity: int) -> list[Individual]:
        if not self.sorted:
            self.population.sort(reverse=True)
            self.sorted = True
        return self.population[:quantity]
    
    def add_individuals(self, individuals: list[Individual]) -> None:
        self.population.extend(individuals)
        self.sorted = False

    def set_population(self, population: list[Individual]) -> None:
        self.population = population
    
    def get_population(self) -> list[Individual]:
        return self.population

    def get_gen_number(self) -> int:
        return self.gen_number
    
    def get_average_fitness(self) -> float:
        fitness_sum = 0.0
        for individual in self.population:
            fitness_sum += individual.fitness_value
        return fitness_sum / len(self.population)

class Environment:
    def __init__(self,
                 objective: Image.Image,
                 hyper_parameters: HyperParameters
    ) -> None:
        self.current_generation = Generation(0)

        self.cap_population_size = hyper_parameters.cap_population_size
        self.fitness_function = hyper_parameters.fitness_function
        self.top_individuals_percentage =\
            hyper_parameters.top_individuals_percentage
        self.crossover_function = hyper_parameters.crossover_function
        self.mutation_probability = hyper_parameters.mutation_probability
        self.mutation_quantity = hyper_parameters.mutation_quantity

        self.objective = objective
        initial_population = self.generate_initial_population()
        self.current_generation.set_population(initial_population)
    
    def generate_initial_population(self) -> list[Individual]:
        print("Generating initial population!")
        population: list[Individual] = []
        for _ in range(self.cap_population_size):
            figure_quantity = random.randint(1, 5)
            individual = Individual(figure_quantity)
            individual.get_genotype().randomize_figures()

            population.append(individual)

        return population
    
    def calculate_fitness(self) -> None:
        for individual in self.current_generation.get_population():
            individual_fitness: float =\
                self.fitness_function(self.objective, individual.get_fenotype())
            individual.set_fitness_value(individual_fitness)

        print("\tPopulation has an average fitness of "
              f"{self.get_current_generation().get_average_fitness()}")

    def get_top_individuals(self) -> list[Individual]:
        quantity = math.floor(self.top_individuals_percentage * self.cap_population_size)
        return self.current_generation.get_top_individuals(quantity)
    
    def get_top_n_individuals(self, quantity: int) -> list[Individual]:
        return self.current_generation.get_top_individuals(quantity)
    
    def get_current_population(self) -> list[Individual]:
        return self.current_generation.get_population()
    
    def cross_top_individuals(self) -> list[Individual]:
        top_individuals = self.get_top_individuals()
        fathers = top_individuals[:len(top_individuals)//2]
        mothers = top_individuals[len(top_individuals)//2:]

        if len(top_individuals) % 2 == 1:
            mothers.append(random.choice(top_individuals))
            fathers.append(top_individuals[-1])

        offspring = []
        for i in range(len(fathers)):
            child = self.crossover_function(fathers[i], mothers[i])
            child.set_parents((fathers[i], mothers[i]))
            offspring.append(child)
        
        return offspring
    
    def mutate_individuals(self, individuals_to_mutate: list[Individual]) -> None:
        for individual in individuals_to_mutate:
            individual.mutate(
                self.mutation_probability,
                self.mutation_quantity
            )
    
    def get_gen_number(self) -> int:
        return self.current_generation.get_gen_number()
    
    def get_current_generation(self) -> Generation:
        return self.current_generation

    def get_best_fenotype(self) -> Image.Image:
        best_ind = self.get_top_n_individuals(1)[0]
        return best_ind.get_fenotype()

    def evolve(self) -> None:
        print("Evolving to next gen!")
        self.calculate_fitness()
        offspring = self.cross_top_individuals()
        self.mutate_individuals(offspring)
        self.current_generation.add_individuals(offspring)

        print("Calculating fitness of all individuals")
        self.calculate_fitness()

        next_gen_individuals =\
            self.get_top_n_individuals(self.cap_population_size)
        self.current_generation = Generation(
            self.get_gen_number() + 1,
            next_gen_individuals)


def run_genetic(env: Environment) -> None:
    for _ in range(hyper_parameters.max_gen):
        best_gen_fenotype = env.get_best_fenotype()
        best_gen_fenotype.save(f"generated_imgs/gen_{env.get_gen_number()}.png")
        env.evolve()

    print("Reached max gen!")

def start_genetic(objective_image: Image.Image,
                hyper_parameters: HyperParameters) -> Environment:
    print("Will start the genetic algorithm!")
    env = Environment(objective_image, hyper_parameters)
    run_genetic(env)
    return env

def continue_genetic_execution(env: Environment) -> Environment:
    print("Will continue executing!")
    run_genetic(env)
    return env

if __name__ == "__main__":
    from fitness_functions import ssim_fitness
    from crossover_functions import one_point_crossover
    objective_image = Image.open('test/objective_1.png')
    hyper_parameters = HyperParameters(
        fitness_function=ssim_fitness,
        crossover_function=one_point_crossover,
        cap_population_size=50,
        top_individuals_percentage=0.5,
        mutation_probability=0.7,
        mutation_quantity=.3,
        max_gen=1000)

    continue_exe = True
    env = start_genetic(objective_image, hyper_parameters)
    while continue_exe:
        print("Finished execution! Want to continue? (y/n)")
        continue_exe = input() == 'y'
        if continue_exe:
            continue_genetic_execution(env)