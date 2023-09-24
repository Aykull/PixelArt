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


def two_point_crossover(
    individual1: Individual, individual2: Individual, current_gen: int
) -> Individual:
    individual1_figures = individual1.get_figures()
    individual2_figures = individual2.get_figures()
    son_figure_quantity = random.choice([len(individual1_figures) - 1,
                                         len(individual2_figures) - 1])
    crossover_point_1 = random.randint(0, son_figure_quantity)
    crossover_point_2 = random.randint(crossover_point_1, son_figure_quantity)

    parent1_figures_point_1 = individual1.get_figures()[:crossover_point_1]
    parent1_figures_point_2 = individual1.get_figures()[crossover_point_2:]

    #if len(individual1_figures) < crossover_point_1:
    #    figures_difference = crossover_point - len(individual1_figures)
    #    crossover_point = crossover_point - figures_difference
    
    parent2_figures = individual2_figures[crossover_point_1:crossover_point_2]

    #parent1_figures = individual1_figures[:crossover_point]
    son_figures = parent1_figures_point_1 + parent2_figures + parent1_figures_point_2
    return Individual(son_figure_quantity, current_gen + 1, son_figures)


def uniform_crossover(
    individual1: Individual, individual2: Individual, current_gen: int
) -> Individual:
    individual1_figures = individual1.get_figures()
    individual2_figures = individual2.get_figures()
    son_figure_quantity = random.choice([len(individual1_figures) - 1,
                                         len(individual2_figures) - 1])
    son_figures = []
    for i in range(1,len(individual1_figures)):
        if random.random() < 0.5:

            individual1_figures = individual1.get_figures()[:i]
            son_figures = son_figures + individual1_figures
        else:
            individual2_figures = individual2.get_figures()[:i]
            son_figures = son_figures + individual2_figures
    
    return Individual(son_figure_quantity, current_gen + 1, son_figures)