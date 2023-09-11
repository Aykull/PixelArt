import unittest
from typing import Any
import random        
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

class TestEnvironment(unittest.TestCase):
    objective_1:Image.Image
    hyper_parameters:HyperParameters
    persisten_env:Environment

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.objective_1 = Image.open('test/objective_1.png')
        cls.hyper_parameters = HyperParameters(
            dummy_fitness_function,
            50)
        cls.persisten_env = Environment(cls.objective_1, HyperParameters(dummy_fitness_function))
    
    def test_environment_should_exist(self) -> None:
        self.assertIsNotNone(self.persisten_env)
    
    def test_initial_population_should_exist(self) -> None:
        population = self.persisten_env.get_current_population()
        self.assertIsNotNone(population)
        self.assertEqual(len(population), 50)
    
    def assertTopIndividuals(self, top_individuals:list[Individual]) -> None:
        self.assertTrue(is_sorted(top_individuals),
                        "Individuals are not sorted in descending order:\n"
                        f"{top_individuals}")

    def test_should_get_top_10_individuals(self) -> None:
        top_indviduals = self.persisten_env.get_top_individuals(10)
        self.assertEqual(len(top_indviduals), 10)
        self.assertTopIndividuals(top_indviduals)
    
    def test_should_cross_individuals(self) -> None:
        pass
        