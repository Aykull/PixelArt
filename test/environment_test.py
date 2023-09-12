import unittest
from typing import Any
import random        
import math
from PIL import Image

from environment import Environment, HyperParameters
from individual import Individual

def is_sorted(array:list[Any]) -> bool:
    if len(array) <= 1:
        return True

    for i in range(1, len(array)):
        if array[i-1] < array[i]:
            return False

    return True 

def dummy_fitness_function(objective:Image.Image, individual:Individual) -> float:
    return random.random()

def dummy_crossover_function(father:Individual, mother:Individual) -> Individual:
    return Individual(5)

class TestEnvironment(unittest.TestCase):
    objective_1:Image.Image
    hyper_parameters:HyperParameters
    persistent_env:Environment

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.objective_1 = Image.open('test/objective_1.png')
        cls.hyper_parameters = HyperParameters(
            dummy_fitness_function,
            dummy_crossover_function,
            cap_population_size=50,
            top_individuals_percentage=0.5,
            mutation_probability=1.0,
            mutation_quantity=1.0)
        cls.persistent_env = Environment(cls.objective_1,
                                         cls.hyper_parameters)
    
    def test_environment_should_exist(self) -> None:
        self.assertIsNotNone(self.persistent_env)
    
    def test_initial_population_should_exist(self) -> None:
        population = self.persistent_env.get_current_population()
        self.assertIsNotNone(population)
        self.assertEqual(len(population), 50)
    
    def assertTopIndividuals(self, top_individuals:list[Individual]) -> None:
        self.assertTrue(is_sorted(top_individuals),
                        "Individuals are not sorted in descending order:\n"
                        f"{top_individuals}")

    def test_should_get_top_n_individuals(self) -> None:
        expected_len = math.floor(self.hyper_parameters.cap_population_size *\
            self.hyper_parameters.top_individuals_percentage)
        top_indviduals = self.persistent_env.get_top_individuals()
        self.assertEqual(len(top_indviduals), expected_len)
        self.assertTopIndividuals(top_indviduals)
    
    def test_should_cross_top_individuals(self) -> None:
        top_individuals = self.persistent_env.get_top_individuals()
        offspring = self.persistent_env.cross_top_individuals()
        for individual in offspring:
            print(f"Checking individual: {individual}")
            self.assertIsNotNone(individual)
            father, mother = individual.get_parents()
            self.assertIn(father, top_individuals,
                          "Father is not in top individuals")
            self.assertIn(mother, top_individuals,
                          "Mother is not in top individuals")
    
    def test_should_mutate_offspring(self) -> None:
        offspring = self.persistent_env.cross_top_individuals()
        self.persistent_env.mutate_individuals(offspring)
        for individual in offspring:
            self.assertTrue(individual.is_mutated(),
                            "Individual did not mutate")
    
    def test_should_generate_new_gen(self) -> None:
        past_gen = self.persistent_env.get_current_generation()

        self.persistent_env.evolve()

        current_gen = self.persistent_env.get_current_generation()
        self.assertEqual(self.persistent_env.get_gen_number(),
                         1, "Generation number stayed the same")
        self.assertNotEqual(past_gen, current_gen,
                            "Current generation is the same as past generation")
        self.assertEqual(len(current_gen.get_population()), self.hyper_parameters.cap_population_size,
                         "Past generation overpassed the population size")