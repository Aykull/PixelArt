from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Generation, HyperParameters
    from individual import Individual

def top_survive(generation: 'Generation',
                hyper_parameters: 'HyperParameters'
) -> list['Individual']:
    cap = hyper_parameters.cap_population_size
    return generation.get_top_individuals(cap)

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
        
    return selected_individuals[:hyper_parameters.cap_population_size]