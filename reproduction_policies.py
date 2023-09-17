import math
import abc

from individual import Individual
from environment import HyperParameters, Generation


class ReproductionPolicy(abc.ABC):
    @abc.abstractmethod
    def reproduce(self, generation: Generation) -> list[Individual]:
        pass


class Elitist(ReproductionPolicy):
    def __init__(self, hyperparameters: HyperParameters) -> None:
        self.hyperparameters = hyperparameters
    
    def reproduce(self, generation: Generation) -> list[Individual]:
        top_individuals = generation.get_top_individuals(
            math.floor(self.hyperparameters.top_individuals_percentage * 
            self.hyperparameters.cap_population_size)
        )
        pairs = self.hyperparameters.match_making_method(top_individuals)
        offspring = []
        for pair in pairs:
            child = self.hyperparameters.crossover_function(
                pair[0], pair[1], generation.get_gen_number())
            child.set_parents((pair[0], pair[1]))
            offspring.append(child)
        return offspring

        