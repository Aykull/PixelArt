from genotype import Genotype

class Environment:
    def __init__(self, initial_population_size=50) -> None:
        self.population: list[Genotype] = []

        self.create_initial_population()
    
    def create_initial_population(self):
        for _ in range(self.initial_population_size):
            self.population.append(
                Genotype(figure)
            )
