import unittest

class TestBasic(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(1, 1)
    
    def test_should_exist_individual(self) -> None:
        individual =  Individual()
        self.assertIsNotNone(individual)
    
    def test_individual_should_have_genes(self) -> None:
        individual = Individual()
        self.assertIsNotNone(individual.get_genes())
    

class Individual():
    def get_genes(self) -> bool:
        return True