import ssim  #type: ignore
from typing import cast
from PIL import Image  #type: ignore

def ssim_fitness(img1:Image.Image, img2:Image.Image) -> float:
    return cast(float, ssim.compute_ssim(img1, img2))


if __name__ == '__main__':
    img1 = Image.open('test/objective_1.png')
    img2 = Image.open('test/objective_1.png')

    print(ssim_fitness(img1, img2))