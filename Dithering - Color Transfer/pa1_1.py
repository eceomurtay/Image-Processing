import cv2
import numpy as np
from pa1_2 import Dithering


def read_img(path):                                     # to read image by using cv2
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)        # turn image into a grayscale image
    return gray


def quantization(img, q):                               # quantize image by using given formula below

    # I_q = round (I / (256/q)) * (256/q)
    q_img = np.uint8(np.round(img / (256 / q)) * (256 / q))
    return q_img


if __name__ == '__main__':

    img1 = read_img("./example images/dithering/1.png")
    quantized = quantization(img1, 16)                      # take q = 16 as quantization parameter
    d = Dithering()                                         # create Dithering class object from pa1_2
    dithered = d.FloydSteinberg(img1, 16)                   # call FloydSteinberg function for dithering
    cv2.imshow("Quantization", quantized)
    cv2.imshow("Floyd-Steinberg Dithering", dithered)
    cv2.waitKey()

