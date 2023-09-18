import unittest
from typing import Any, TYPE_CHECKING
import random        
import math
from PIL import Image #type: ignore

from environment import Environment, HyperParameters
from individual import Individual

if TYPE_CHECKING:
    from environment import Generation

def is_sorted(array:list[Any]) -> bool:
    if len(array) <= 1:
        return True

    for i in range(1, len(array)):
        if array[i-1] < array[i]:
            return False

    return True 

def dummy_fitness_function(objective:Image.Image, individual_image:Image.Image) -> float:
    return random.random()

def dummy_crossover_function(father:Individual, mother:Individual, number: int) -> Individual:
    return Individual(5, 0)

def dummy_match_making_method(individuals:list[Individual]) -> list[tuple[Individual, Individual]]:
    return list(zip(individuals, individuals))

def dummy_survival_function(generation: 'Generation',
                            hyper_parameters: 'HyperParameters'
) -> list[Individual]:
    return generation.get_population()[:hyper_parameters.cap_population_size]

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
            dummy_match_making_method,
            survival_function=dummy_survival_function,
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