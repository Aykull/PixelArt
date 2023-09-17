import unittest

from reproduction_policies import Stratified
from environment import Generation, HyperParameters
from individual import Individual


def match_making_mock(individuals: list[Individual]) -> list[tuple[Individual, Individual]]:
    fathers = individuals[:len(individuals)//2]
    mothers = individuals[len(individuals)//2:]

    return list(x for x in zip(fathers, mothers))


class StratifiedTest(unittest.TestCase):
    def setUp(self) -> None:
        population = [Individual(0, 1) for _ in range(10)]
        self.generation = Generation(3, population=population)
        self.hyperparameters = HyperParameters(
            cap_population_size=10,
            fitness_function=lambda x, y: 0,
            match_making_method=match_making_mock,
            top_individuals_percentage=0.2,
            crossover_function=lambda x, y, z: Individual(0, 1),
            childs_per_pair=2
        )

    def test_stratify_population(self) -> None:
        stratified = Stratified(self.hyperparameters)
        stratas = stratified.stratify_population(self.generation.get_population())

        self.assertEqual(len(stratas), 5)
        self.assertEqual(len(stratas[0]), 2)
        self.assertEqual(len(stratas[1]), 2)
        self.assertEqual(len(stratas[2]), 2)
        self.assertEqual(len(stratas[3]), 2)
        self.assertEqual(len(stratas[4]), 2)
    
    def test_same_length_of_childs(self) -> None:
        stratified = Stratified(self.hyperparameters)
        offspring = stratified.reproduce(self.generation)

        self.assertEqual(len(offspring), len(self.generation.get_population()))