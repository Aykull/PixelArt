from typing import Callable, Union, TYPE_CHECKING
import matplotlib.pyplot as plt
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
    survival_function: Callable[['Generation', 'HyperParameters'], list[Individual]]

    reproduction_policy: Union['ReproductionPolicy', None] = None
    cap_population_size: int = 50
    top_individuals_percentage: float = 0.1
    mutation_probability: float = 0.1
    mutation_quantity: float = 0.1
    max_gen:int = 100
    age_penalty:float = 0.0
    childs_per_pair:int = 3
    parallelize:bool = False

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

    def get_bot_individuals(self, quantity: int) -> list[Individual]:
        if not self.sorted:
            self.population.sort(reverse=True)
            self.sorted = True
        return self.population[quantity:]
    
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
        self.hyper_parameters = hyper_parameters

        self.cap_population_size = hyper_parameters.cap_population_size
        self.fitness_function = hyper_parameters.fitness_function
        self.match_making_method = hyper_parameters.match_making_method
        self.survival_function = hyper_parameters.survival_function

        self.top_individuals_percentage =\
            hyper_parameters.top_individuals_percentage
        self.crossover_function = hyper_parameters.crossover_function
        self.mutation_probability = hyper_parameters.mutation_probability
        self.mutation_quantity = hyper_parameters.mutation_quantity
        self.age_penalty = hyper_parameters.age_penalty

        self.objective = objective
        initial_population = self.generate_initial_population()
        self.current_generation.set_population(initial_population)

        self.highest_fitness: float = 0.0
        self.highest_fit_generation: int = 0



        if not hyper_parameters.reproduction_policy:
            raise ValueError("Reproduction policy not set!")
        self.reproduction_policy = hyper_parameters.reproduction_policy
    
    def generate_initial_population(self) -> list[Individual]:
        print("Generating initial population!")
        population: list[Individual] = []
        for _ in range(self.cap_population_size):
            # figure_quantity = random.randint(3, 10)
            figure_quantity = random.randint(1, 5)
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

            if individual.get_fitness() > self.highest_fitness:
                self.highest_fitness = individual.get_fitness()
                self.highest_fit_generation = individual.get_birth_gen()

        print("\tPopulation has an average fitness of "
              f"{self.get_current_generation().get_average_fitness()}")
        self.current_generation.population.sort(reverse=True)

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

    def evolve(self):
        print("Evolving to next gen!")
        self.calculate_fitness()

        offspring = self.reproduction_policy.reproduce(self.current_generation)

        self.mutate_individuals(offspring)
        self.current_generation.add_individuals(offspring)

        print("Calculating fitness of all individuals")
        self.calculate_fitness()

        next_gen_individuals, dead_population =\
            self.survival_function(self.get_current_generation(), 
                                   self.hyper_parameters)[:self.cap_population_size]

        self.current_generation = Generation(
            self.get_gen_number() + 1,
            next_gen_individuals)
        self.current_generation.age_population()
        dead_population_sort = dict(sorted(dead_population.items()))
        return dead_population_sort


def run_genetic(env: Environment, hyper_parameters: HyperParameters) -> None:
    gen_graph = []
    av_fit_graph = []
    for _ in range(hyper_parameters.max_gen):
        best_individual = env.get_top_n_individuals(1)[0]
        print(f"\tGeneration best individual is {best_individual.name}"
              f" from gen: {best_individual.get_birth_gen()},"
              f" age: {best_individual.get_age()}"
              f" with {best_individual.fitness_value}")
        gen_graph.append(env.get_gen_number())
        av_fit_graph.append(env.get_current_generation().get_average_fitness())
        best_gen_fenotype = best_individual.get_fenotype()
        best_gen_fenotype.save(f"generated_imgs2/gen_{env.get_gen_number()}.png")
        dead_population = env.evolve()
        
    print("Reached max gen!")
    return gen_graph, av_fit_graph, dead_population

def start_genetic(objective_image: Image.Image,
                hyper_parameters: HyperParameters) -> (Environment, list, list):
    print("Will start the genetic algorithm!")
    env = Environment(objective_image, hyper_parameters)
    gen, av_fit, dead = run_genetic(env, hyper_parameters)
    return env, gen, av_fit, dead

def continue_genetic_execution(
    env: Environment, hyper_parameters: HyperParameters
) -> (Environment, list, list):
    print("Will continue executing!")
    gen, av_fit = run_genetic(env, hyper_parameters)
    return env, gen, av_fit


def main() -> None:
    from fitness_functions import ssim_fitness
    from crossover_functions import one_point_crossover
    from match_making_methods import halves, random_shuffle
    from reproduction_policies import Elitist, Stratified
    from survival_functions import top_survive, elite_survive

    objective_image = Image.open('test/objective_3.png')
    hyper_parameters = HyperParameters(
        fitness_function=ssim_fitness,
        crossover_function=one_point_crossover,
        match_making_method=random_shuffle,
        survival_function=top_survive,
        cap_population_size=50,
        top_individuals_percentage=0.2,
        mutation_probability=0.7,
        mutation_quantity=.2,
        max_gen=5_000,
        childs_per_pair=2,
        parallelize=True,
        age_penalty=0.000001)
    hyper_parameters.set_reproduction_policy(Stratified(hyper_parameters))

    continue_exe = True
    env = None
    gen = []
    av_fit = []
    try:
        env, gen, av_fit, dead = start_genetic(objective_image, hyper_parameters)
        while continue_exe:
            print("Finished execution! Want to continue? (y/n)")
            print(f"Highest fitness achieved: {env.highest_fitness}"
                f" in generation: {env.highest_fit_generation}")
            continue_exe = input() == 'y'
            if continue_exe:
                continue_genetic_execution(env, hyper_parameters)
    except Exception:
        if env:
            print(f"Highest fitness achieved: {env.highest_fitness}"
                f" in generation: {env.highest_fit_generation}")
    
    figure, axis = plt.subplots(1, 2, figsize=(12, 5))
    
    axis[0].plot(gen, av_fit, marker='o', linestyle='-')
    axis[0].set_xlabel('Generación')
    axis[0].set_ylabel('Fitness')
    axis[0].set_title('Generación vs. Fitness')

    ages = list(dead.keys())
    population = list(dead.values())
    axis[1].bar(ages, population, align='center')
    axis[1].set_xlabel('Edades')
    axis[1].set_ylabel('Población')
    axis[1].set_title('Edades vs. Población')
    
    plt.show()
    

if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()', sort='cumulative')
    main()