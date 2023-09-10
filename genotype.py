from PIL import Image, ImageDraw, ImageColor
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
        self.figure_quantity = figure_quantity
        self.figures = figures
    
    def randomize_figues(self) -> None:
        pass
    
    def make_fenotype(self) -> Image:
        canvas = Image.new("RGB", CANVAS_SIZE, ImageColor.getrgb("white"))
        draw = ImageDraw.Draw(canvas, "RGBA")
        for figure in self.figures:
            draw.rectangle(
                [figure.initial_point, figure.end_point], fill=figure.color)
        return canvas
