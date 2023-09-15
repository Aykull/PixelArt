import math
import random
from PIL import Image, ImageDraw, ImageColor
from typing import Union
from faker import Faker

from constants import CANVAS_SIZE

class MyRect:
    def __init__(self, initial_point:tuple[int, int], 
                 end_point:tuple[int, int], color:tuple[int, int, int, int])-> None:
        self.initial_point = initial_point
        self.end_point = end_point
        self.color = color
    
    def is_within_bounds(self) -> bool:
        return (self.initial_point[0] < CANVAS_SIZE[0] and
            self.initial_point[1] < CANVAS_SIZE[1] and
            self.end_point[0] < CANVAS_SIZE[0] and
            self.end_point[1] < CANVAS_SIZE[1])
    
    def end_point_is_valid(self) -> bool:
        return (self.initial_point[0] < self.end_point[0] and
            self.initial_point[1] < self.end_point[1])
    
    def color_is_valid(self) -> bool:
        return (self.color[0] >= 0 and self.color[0] <= 255 and
            self.color[1] >= 0 and self.color[1] <= 255 and
            self.color[2] >= 0 and self.color[2] <= 255 and
            self.color[3] >= 0 and self.color[3] <= 255)


class Genotype:
    def __init__(self, figure_quantity: int,
        figures: list[MyRect]=[]
    ) -> None:
        self.figure_quantity:int = figure_quantity
        self.figures = figures
    
    def get_figures(self) -> list[MyRect]:
        return self.figures

    def mutate_fig_quantity(self, mutation_quantity: float) -> None:
        self.figure_quantity = math.ceil(self.figure_quantity + \
            mutation_quantity * self.figure_quantity)
        if self.figure_quantity < 1:
            self.figure_quantity = 1

    def mutate_figure_form(self,
        figure: MyRect, mutation_quantity: float
    ) -> None:
        old_initial_point = figure.initial_point
        old_end_point = figure.end_point 

        figure.initial_point = (
            math.ceil(figure.initial_point[0] +\
                      mutation_quantity * figure.initial_point[0]),
            math.ceil(figure.initial_point[1] +\
                      mutation_quantity * figure.initial_point[1])
        )
        if not figure.is_within_bounds():
            figure.initial_point = old_initial_point
            return

        figure.end_point = (
            math.ceil(figure.end_point[0] +\
                      mutation_quantity * figure.end_point[0]),
            math.ceil(figure.end_point[1] +\
                      mutation_quantity * figure.end_point[1])
        )
        if not figure.end_point_is_valid() or not figure.is_within_bounds():
            figure.end_point = old_end_point
            if not figure.end_point_is_valid():
                figure.initial_point = old_initial_point
        
        return
    
    def mutate_figure_color(self,
        figure: MyRect, mutation_quantity: float
    ) -> None:
        old_color = figure.color
        figure.color = (
            math.ceil(figure.color[0] + mutation_quantity * figure.color[0]),
            math.ceil(figure.color[1] + mutation_quantity * figure.color[1]),
            math.ceil(figure.color[2] + mutation_quantity * figure.color[2]),
            math.ceil(figure.color[3] + mutation_quantity * figure.color[3])
        )
        if not figure.color_is_valid():
            figure.color = old_color

    def mutate(self,
        mutation_probability: float,
        mutation_quantity: float
    ) -> bool:
        mutated = False
        mutation_quantity = random.choice([-1, 1]) * mutation_quantity

        if random.random() < mutation_probability:
            mutated = True
            self.mutate_fig_quantity(mutation_quantity)
        
        for figure in self.figures:
            if random.random() < mutation_probability:
                mutated = True
                self.mutate_figure_form(figure, mutation_quantity)
            
            if random.random() < mutation_probability:
                mutated = True
                self.mutate_figure_color(figure, mutation_quantity)
        
        return mutated
    
    def randomize_figures(self) -> None:
        for _ in range(self.figure_quantity):
            initial_point = (
                random.randint(0, CANVAS_SIZE[0]-1),
                random.randint(0, CANVAS_SIZE[1]-1))

            figure = MyRect(
                initial_point = initial_point,
                end_point = (random.randint(initial_point[0], CANVAS_SIZE[0]),
                    random.randint(initial_point[1], CANVAS_SIZE[1])),
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255))
            )
            self.figures.append(figure)

class Individual:
    def __init__(self,
        figure_quantity:int, figures: list[MyRect]=[]
    ) -> None:
        self.genotype = Genotype(figure_quantity, figures)

        self.fenotype:Union[Image.Image, None] = None
        self.fitness_value:float = 0
        self.name:str = Faker().name()
        self.mutated:bool = False
        self.parents:Union[tuple['Individual', 'Individual'], None] = None

    def mutate(self, mutation_probability: float,
        mutation_quantity: float
    ) -> None:
        self.mutated =\
            self.genotype.mutate(mutation_probability, mutation_quantity)

    def is_mutated(self) -> bool:
        return self.mutated

    def set_fitness_value(self, fitness_value: float) -> None:
        self.fitness_value = fitness_value
    
    def get_fenotype(self) -> Image.Image:
        if self.fenotype is None:
            self.fenotype = self.make_fenotype()
        
        return self.fenotype
    
    def get_genotype(self) -> Genotype:
        return self.genotype

    def get_figures(self) -> list[MyRect]:
        return self.genotype.get_figures()
    
    def get_parents(self) -> tuple['Individual', 'Individual']:
        if self.parents is None:
            raise Exception("Parents not set")
        return self.parents

    def set_parents(self, parents: tuple['Individual', 'Individual']) -> None:
        if self.parents is None:
            self.parents = parents
        else:
            raise Exception("Parents already set")
    
    def make_fenotype(self) -> Image.Image:
        canvas = Image.new("RGB", CANVAS_SIZE, ImageColor.getrgb("white"))
        draw = ImageDraw.Draw(canvas, "RGBA")
        for figure in self.get_figures():
            draw.rectangle(
                (figure.initial_point, figure.end_point),
                fill=figure.color)
        return canvas
    
    def __lt__(self, other:'Individual') -> bool:
        return self.fitness_value < other.fitness_value
    
    def __le__(self, other:'Individual') -> bool:
        return self.fitness_value <= other.fitness_value
    
    def __gt__(self, other:'Individual') -> bool:
        return self.fitness_value > other.fitness_value
    
    def __ge__(self, other:'Individual') -> bool:
        return self.fitness_value >= other.fitness_value

    def __str__(self) -> str:
        return f"Name: {self.name}\nFitness value: {self.fitness_value:.2f}\n"
    
    def __repr__(self) -> str:
        return self.__str__()

