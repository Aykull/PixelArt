import ssim  #type: ignore
from typing import cast
from PIL import Image  #type: ignore
import numpy as np
import cv2

def ssim_fitness(img1:Image.Image, img2:Image.Image) -> float:
    return cast(float, ssim.compute_ssim(img1, img2))


def mse(img_mse_1, img_mse_2):
    dif = cv2.absdiff(img_mse_1, img_mse_2)
    dif = dif.astype(np.float32) 
    dif = dif ** 2
    mse = np.mean(dif)
    return mse


if __name__ == '__main__':
    img1 = Image.open('test/objective_1.png')
    img2 = Image.open('test/objective_1.png')

    img_mse_1 = cv2.imread('test/objective_1.png')
    img_mse_2 = cv2.imread('test/objective_1.png')
    img_mse_3 = cv2.imread('test/objective_2.png')

    print(ssim_fitness(img1, img2))
    # 0 -> ajuste perfecto
    print(mse(img_mse_1,img_mse_2))
    print(mse(img_mse_1,img_mse_3))