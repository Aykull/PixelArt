import math
import random
import abc

from individual import Individual
from environment import HyperParameters, Generation


class ReproductionPolicy(abc.ABC):
    def __init__(self, hyperparameters: HyperParameters) -> None:
        self.hyperparameters = hyperparameters

    def _crossover_pairs(
        self, pairs: list[tuple[Individual, Individual]], gen_number: int
    ) -> list[Individual]:
        offspring = []
        for pair in pairs:
            pair_childs = []
            for _ in range(self.hyperparameters.childs_per_pair):
                child = self.hyperparameters.crossover_function(
                    pair[0], pair[1], gen_number)
                child.set_parents((pair[0], pair[1]))
                pair_childs.append(child)
            offspring.extend(pair_childs)
        return offspring

    @abc.abstractmethod
    def reproduce(self, generation: Generation) -> list[Individual]:
        pass


class Elitist(ReproductionPolicy):
    def reproduce(self, generation: Generation) -> list[Individual]:
        top_individuals = generation.get_top_individuals(
            math.floor(self.hyperparameters.top_individuals_percentage * 
            self.hyperparameters.cap_population_size)
        )
        if len(top_individuals) % 2 == 1:
            top_individuals.append(random.choice(top_individuals))

        pairs = self.hyperparameters.match_making_method(top_individuals)

        return self._crossover_pairs(pairs, generation.get_gen_number())

class Stratified(ReproductionPolicy):
    def stratify_population(
        self, population: list[Individual]
    ) -> list[list[Individual]]:
        strata_cut = math.floor(self.hyperparameters.top_individuals_percentage * 
            self.hyperparameters.cap_population_size)
        stratas = []
        for i in range(0, len(population), strata_cut):
            stratas.append(population[i:i+strata_cut])
        return stratas

    def reproduce(self, generation: Generation) -> list[Individual]:
        stratas = self.stratify_population(generation.get_population())
        offspring = []
        for strata in stratas:
            if len(strata) % 2 == 1:
                strata.append(random.choice(strata))

            pairs = self.hyperparameters.match_making_method(strata)
            strata_offspring = self._crossover_pairs(
                pairs, generation.get_gen_number())
            offspring.extend(strata_offspring)
        return offspring

        