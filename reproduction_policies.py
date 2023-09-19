import math
import random
import abc
import multiprocessing
from contextlib import closing
from typing import Callable

from individual import Individual
from environment import HyperParameters, Generation

def crossover_worker(
    pairs: list[tuple[Individual, Individual]],
    childs_per_pair: int,
    gen_number: int,
    crossover_function: Callable[[Individual, Individual, int], Individual]
) -> list[Individual]:
    offspring = []
    for pair in pairs:
        pair_childs = []
        for _ in range(childs_per_pair):
            child = crossover_function(
                pair[0], pair[1], gen_number)
            pair_childs.append(child)
        offspring.extend(pair_childs)
    return offspring

class ReproductionPolicy(abc.ABC):
    def __init__(self, hyperparameters: HyperParameters) -> None:
        self.hyperparameters = hyperparameters
    
    def _crossover_pairs_parallel(
        self, pairs: list[tuple[Individual, Individual]], gen_number: int
    ) -> list[Individual]:

        num_processes = math.ceil(multiprocessing.cpu_count() / 2)
        
        chunks = [pairs[i::num_processes] for i in range(num_processes)]
        offspring: list[Individual] = []
        arguments = [(chunk, self.hyperparameters.childs_per_pair, gen_number,
                      self.hyperparameters.crossover_function)
                     for chunk in chunks]

        with closing(multiprocessing.Pool(processes=num_processes)) as pool:
            worker_offsprings: list[list[Individual]] =\
                pool.starmap(crossover_worker, arguments)
            pool.close()
        
        for worker_offspring in worker_offsprings:
            offspring.extend(worker_offspring)
        
        return offspring
        

    def _crossover_pairs(
        self, pairs: list[tuple[Individual, Individual]], gen_number: int
    ) -> list[Individual]:
        """
        This operation is compute intensive, so we are parallelizing it.
        In order to take the most out of this parallelization we should pass as
        pairs all the individuals we are going to cross for this generation.
        """
        print(f"\t Will reproduce {len(pairs)} pairs")

        if self.hyperparameters.parallelize:
            return self._crossover_pairs_parallel(pairs, gen_number)
        else:
            return crossover_worker(pairs, self.hyperparameters.childs_per_pair,
                                    gen_number, self.hyperparameters.crossover_function) 
        

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
        pairs = []
        for strata in stratas:
            if len(strata) % 2 == 1:
                strata.append(random.choice(strata))
            pairs.extend(self.hyperparameters.match_making_method(strata))
        
        offspring = self._crossover_pairs(pairs, generation.get_gen_number())
        return offspring

        