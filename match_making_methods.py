import random
from individual import Individual

def halves(
    individuals:list[Individual]
) -> list[tuple[Individual, Individual]]:
    fathers = individuals[:len(individuals)//2]
    mothers = individuals[len(individuals)//2:]

    return list(x for x in zip(fathers, mothers))

def random_shuffle(
    individuals: list[Individual]
) -> list[tuple[Individual, Individual]]:
    random.shuffle(individuals)
    fathers = individuals[:len(individuals)//2]
    mothers = individuals[len(individuals)//2:]

    return list(x for x in zip(fathers, mothers))

