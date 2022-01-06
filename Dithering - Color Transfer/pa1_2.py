"""
Floyd-Steinberg dithering
"""

import numpy as np


class Dithering:

    @staticmethod
    def find_quantized_value(pixel, q):             # by using q parameter find the quantized value

        return np.round(q * pixel / 255) * (255 / q)

    def FloydSteinberg(self, image, q):

        output = np.copy(image)                     # copy the original image to not to damage it
        height, width = image.shape

        for h in range(1, height - 1):
            for w in range(1, width - 1):
                old_pixel = output[h][w]
                new_pixel = self.find_quantized_value(old_pixel, q)         # quantized value of old pixel
                output[h][w] = new_pixel
                quant_error = old_pixel - new_pixel

                output[h][w + 1] += quant_error * 7 / 16
                output[h + 1][w - 1] += quant_error * 3 / 16
                output[h + 1][w] += quant_error * 5 / 16
                output[h + 1][w + 1] += quant_error * 1 / 16

        return output

