import random
from individual import Individual

def one_point_crossover(
    individual1: Individual, individual2: Individual, current_gen: int
) -> Individual:
    individual1_figures = individual1.get_figures()
    individual2_figures = individual2.get_figures()
    son_figure_quantity = random.choice([len(individual1_figures),
                                         len(individual2_figures)])
    crossover_point = random.randint(0, son_figure_quantity)

    parent1_figures = individual1.get_figures()[:crossover_point]

    if len(individual1_figures) < crossover_point:
        figures_difference = crossover_point - len(individual1_figures)
        crossover_point = crossover_point - figures_difference
    
    parent2_figures = individual2_figures[crossover_point:]

    parent1_figures = individual1_figures[:crossover_point]
    son_figures = parent1_figures + parent2_figures
    return Individual(son_figure_quantity, current_gen + 1, son_figures)