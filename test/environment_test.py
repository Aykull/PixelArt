import unittest

from environment import Environment

class TestEnvironment(unittest.TestCase):
    def test_environment_should_exist(self) -> None:
        environment = Environment()
        self.assertIsNotNone(environment)
    
    def test_initial_population_should_exist(self) -> None:
        environment = Environment()
        self.assertIsNotNone(environment.population)
        self.assertEqual(len(environment.population), 50)
    
