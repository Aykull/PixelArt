from typing import Callable, Union, TYPE_CHECKING
import random
import math
from PIL import Image  #type: ignore
from dataclasses import dataclass

from individual import Individual 


if TYPE_CHECKING:
    from reproduction_policies import ReproductionPolicy


@dataclass
class HyperParameters:
    fitness_function: Callable[[Image.Image, Image.Image], float]
    crossover_function: Callable[[Individual, Individual, int], Individual]
    match_making_method: Callable[[list[Individual]], list[tuple[Individual,
                                                                 Individual]]]
    reproduction_policy: Union['ReproductionPolicy', None] = None
    cap_population_size: int = 50
    top_individuals_percentage: float = 0.1
    mutation_probability: float = 0.1
    mutation_quantity: float = 0.1
    max_gen:int = 100
    age_penalty:float = 0.0

    def set_reproduction_policy(self, reproduction_policy: 'ReproductionPolicy') -> None:
        self.reproduction_policy = reproduction_policy


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

    def age_population(self) -> None:
        for individual in self.population:
            if individual.get_birth_gen() != self.gen_number:
                individual.turn_older()

class Environment:
    def __init__(self,
                 objective: Image.Image,
                 hyper_parameters: HyperParameters
    ) -> None:
        self.current_generation = Generation(0)

        self.cap_population_size = hyper_parameters.cap_population_size
        self.fitness_function = hyper_parameters.fitness_function
        self.match_making_method = hyper_parameters.match_making_method
        self.top_individuals_percentage =\
            hyper_parameters.top_individuals_percentage
        self.crossover_function = hyper_parameters.crossover_function
        self.mutation_probability = hyper_parameters.mutation_probability
        self.mutation_quantity = hyper_parameters.mutation_quantity
        self.age_penalty = hyper_parameters.age_penalty

        self.objective = objective
        initial_population = self.generate_initial_population()
        self.current_generation.set_population(initial_population)

        if not hyper_parameters.reproduction_policy:
            raise ValueError("Reproduction policy not set!")
        self.reproduction_policy = hyper_parameters.reproduction_policy
    
    def generate_initial_population(self) -> list[Individual]:
        print("Generating initial population!")
        population: list[Individual] = []
        for _ in range(self.cap_population_size):
            figure_quantity = random.randint(3, 10)
            individual = Individual(figure_quantity, 0)
            individual.get_genotype().randomize_figures()

            population.append(individual)

        return population
    
    def _apply_age_penalty(self, individual: Individual) -> None:
        individual.fitness_value = (individual.fitness_value -
                                    self.age_penalty * individual.get_age())
        if individual.fitness_value < 0:
            individual.fitness_value = 0

    def calculate_fitness(self) -> None:
        for individual in self.current_generation.get_population():
            individual_fitness: float =\
                self.fitness_function(self.objective, individual.get_fenotype())
            individual.set_fitness_value(individual_fitness)
            self._apply_age_penalty(individual)

        print("\tPopulation has an average fitness of "
              f"{self.get_current_generation().get_average_fitness()}")

    def get_top_individuals(self) -> list[Individual]:
        quantity = math.floor(self.top_individuals_percentage * self.cap_population_size)
        return self.current_generation.get_top_individuals(quantity)
    
    def get_top_n_individuals(self, quantity: int) -> list[Individual]:
        return self.current_generation.get_top_individuals(quantity)
    
    def get_current_population(self) -> list[Individual]:
        return self.current_generation.get_population()
    
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

        offspring = self.reproduction_policy.reproduce(self.current_generation)

        self.mutate_individuals(offspring)
        self.current_generation.add_individuals(offspring)

        print("Calculating fitness of all individuals")
        self.calculate_fitness()

        next_gen_individuals =\
            self.get_top_n_individuals(self.cap_population_size)
        self.current_generation = Generation(
            self.get_gen_number() + 1,
            next_gen_individuals)
        self.current_generation.age_population()


def run_genetic(env: Environment) -> None:
    for _ in range(hyper_parameters.max_gen):
        best_individual = env.get_top_n_individuals(1)[0]
        print(f"\tGeneration best individual is {best_individual.name}"
              f" from gen: {best_individual.get_birth_gen()},"
              f" age: {best_individual.get_age()}"
              f" with {best_individual.fitness_value}")
        best_gen_fenotype = best_individual.get_fenotype()
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
    from match_making_methods import halves
    from reproduction_policies import Elitist
    objective_image = Image.open('test/objective_1.png')
    hyper_parameters = HyperParameters(
        fitness_function=ssim_fitness,
        crossover_function=one_point_crossover,
        match_making_method=halves,
        cap_population_size=50,
        top_individuals_percentage=0.2,
        mutation_probability=0.7,
        mutation_quantity=.2,
        max_gen=100_000,
        age_penalty=0.0)
    hyper_parameters.set_reproduction_policy(Elitist(hyper_parameters))

    continue_exe = True
    env = start_genetic(objective_image, hyper_parameters)
    while continue_exe:
        print("Finished execution! Want to continue? (y/n)")
        continue_exe = input() == 'y'
        if continue_exe:
            continue_genetic_execution(env)