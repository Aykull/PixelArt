from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Generation, HyperParameters
    from individual import Individual

def top_survive(generation: 'Generation',
                hyper_parameters: 'HyperParameters'
) -> (list['Individual'], dict):
    cap = hyper_parameters.cap_population_size
    dead_population = create_graph_dir(generation.get_bot_individuals(cap))
    
    return generation.get_top_individuals(cap), dead_population

def elite_survive(generation: 'Generation',
                  hyper_parameters:'HyperParameters'
) -> (list['Individual'], dict):
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
    dead_population = create_graph_dir(selected_individuals[hyper_parameters.cap_population_size:])
    return selected_individuals[:hyper_parameters.cap_population_size], dead_population

graph_dir = {}
def create_graph_dir(dead_population):
    count = 0
    for population in dead_population:
        count = count + 1
        graph_dir[population.get_age()] = count
    return graph_dir
    