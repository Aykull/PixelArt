from PIL import Image, ImageDraw, ImageColor
from typing import Union
from faker import Faker

from constants import CANVAS_SIZE

class MyRect:
    def __init__(self, initial_point:tuple[int, int], 
                 end_point:tuple[int, int], color:tuple[int, int, int])-> None:
        self.initial_point = initial_point
        self.end_point = end_point
        self.color = color


class Genotype:
    def __init__(self, figure_quantity: int,
                 figures: list[MyRect]=[]
    ) -> None:
        self.figure_quantity:int = figure_quantity
        self.figures = figures
    
    def get_figures(self) -> list[MyRect]:
        return self.figures

class Individual:
    def __init__(self,
                 figure_quantity:int,
                 figures: list[MyRect]=[]) -> None:
        self.genotype = Genotype(figure_quantity, figures)

        self.fenotype:Union[Image.Image, None] = None
        self.fitness_value:float = 0
        self.name:str = Faker().name()
        self.mutated:bool = False
        self.parents:Union[tuple[Genotype, Genotype], None] = None
    
    def set_fitness_value(self, fitness_value: float) -> None:
        self.fitness_value = fitness_value
    
    def get_fenotype(self) -> Image.Image:
        if self.fenotype is None:
            self.fenotype = self.make_fenotype()
        
        return self.fenotype
    
    def get_figures(self) -> list[MyRect]:
        return self.genotype.get_figures()
    
    def randomize_figures(self) -> None:
        pass
    
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

