from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from environment import Generation, HyperParameters
    from individual import Individual

def top_survive(generation: 'Generation',
                hyper_parameters: 'HyperParameters'
) -> list['Individual']:
    cap = hyper_parameters.cap_population_size
    next_population = generation.get_top_individuals(cap)
    update_dead_graph(generation.get_population()[cap:])
    
    return next_population

def elite_survive(generation: 'Generation',
                  hyper_parameters:'HyperParameters'
) -> list['Individual']:
    population = generation.get_population()
    elite_cut = int(len(population) *
                    hyper_parameters.top_individuals_percentage)
    
    selected_individuals: list['Individual'] = population
    old_individuals: list['Individual'] = []

    for individual in population[elite_cut:]:
        if not individual.is_from_gen(generation.get_gen_number() + 1):
            selected_individuals.remove(individual)
            old_individuals.append(individual)
    
    old_individuals.sort(key=lambda x:x.age)
    selected_individuals.extend(old_individuals)
    update_dead_graph(selected_individuals[hyper_parameters.cap_population_size:])
    return selected_individuals[:hyper_parameters.cap_population_size]

dead_graph:dict[int, int] = {}
def update_dead_graph(dead_population: list['Individual']) -> None:
    global dead_graph
    for individual in dead_population:
        if individual.get_age() not in dead_graph:
            dead_graph[individual.get_age()] = 0
        dead_graph[individual.get_age()] += 1

def get_dead_graph() -> dict[int, int]:
    global dead_graph
    return dead_graph
    