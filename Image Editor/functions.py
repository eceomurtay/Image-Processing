# Import required Image library
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import PIL.ImageOps
import cv2


class ImageFunctions:

    def __init__(self, path):
        self.path = path

    def blur_Image(self, blur_type):
        # Open existing image
        img = Image.open(self.path)

        if blur_type == 'simple':
            simpleBlur = img.filter(ImageFilter.BLUR)
            return simpleBlur

        elif blur_type == 'box':
            boxBlur = img.filter(ImageFilter.BoxBlur(5))
            return boxBlur

        elif blur_type == 'gaussian':
            gaussianBlur = img.filter(ImageFilter.GaussianBlur(5))
            return gaussianBlur

    def deblur_Image(self):
        # Open existing image
        img = Image.open(self.path)
        # Apply sharp filter
        sharpened1 = img.filter(ImageFilter.SHARPEN)
        sharpened2 = sharpened1.filter(ImageFilter.SHARPEN)
        return sharpened2

    def flip_Image(self, flipType):
        # Open existing image
        img = Image.open(self.path)

        if flipType == 'horizontal':
            # Do a flip of left and right
            horiFlippedImage = img.transpose(Image.FLIP_LEFT_RIGHT)
            return horiFlippedImage

        elif flipType == 'vertical':
            # Show vertically flipped image
            VertFlippedImage = img.transpose(Image.FLIP_TOP_BOTTOM)
            return VertFlippedImage

        elif flipType == 'clockwise':
            flipImage = img.transpose(Image.TRANSVERSE)
            return flipImage

        elif flipType == 'anticlockwise':
            flipImage = img.transpose(Image.TRANSPOSE)
            return flipImage

    def rotate_Image(self, degree):
        # Open existing image
        img = Image.open(self.path)

        if degree == 90:
            rot90Image = img.transpose(Image.ROTATE_90)
            return rot90Image

        elif degree == 270:
            rot270Image = img.transpose(Image.ROTATE_270)
            return rot270Image

        else:
            rotatedImage = img.rotate(degree, expand=True)
            return rotatedImage

    def add_noise(self, noiseType):

        # Open existing image
        img = cv2.imread(self.path)
        result = np.copy(np.array(img))

        if noiseType == 'gauss':
            # Generate Gaussian noise
            gauss = np.random.normal(0, 1, result.size)
            gauss = gauss.reshape((result.shape[0], result.shape[1], result.shape[2])).astype('uint8')
            # Add the Gaussian noise to the image
            img_gauss = cv2.add(result, gauss)
            return img_gauss

        elif noiseType == 'speckle':
            speckle = np.random.normal(0, 1, result.size)
            speckle = speckle.reshape((result.shape[0], result.shape[1], result.shape[2])).astype('uint8')
            img_speckle = result + result * speckle
            return img_speckle

    def change_color_balance(self, val):

        img = Image.open(self.path)
        [xs, ys] = img.size
        # For loop to extract and print all pixels
        for x in range(0, xs):
            for y in range(0, ys):
                # getting pixel value using getpixel() method
                [r, g, b] = img.getpixel((x, y))
                r = r + val
                g = g + val
                b = b + val
                value = (r, g, b)
                img.putpixel((x, y), value)

        return img

    def reverse_color(self):

        img = Image.open(self.path)
        inverted_img = PIL.ImageOps.invert(img)
        return inverted_img

    def adjust_brightness(self, factor):

        img = Image.open(self.path)
        # image brightness enhancer
        enhancer = ImageEnhance.Brightness(img)

        # if factor > 1   brightens the image otherwise darkens
        adjusted = enhancer.enhance(factor)
        return adjusted

    def adjust_saturation(self, factor):

        img = Image.open(self.path)
        converter = PIL.ImageEnhance.Color(img)
        saturation_adjusted = converter.enhance(factor)
        return saturation_adjusted

    def adjust_contrast(self, factor):
        # Open existing image
        img = Image.open(self.path)
        imgObj = ImageEnhance.Contrast(img)
        contImg = imgObj.enhance(factor)
        return contImg

    def mirror_image(self):
        # Open existing image
        img = Image.open(self.path)
        mirror_img = PIL.ImageOps.mirror(img)
        return mirror_img

    def detect_edges(self):
        # Open
        img = Image.open(self.path)
        img_gray = img.convert("L")
        # ImageFilter.FIND_EDGE uses 3 X 3 sized Laplacian kernel
        edges = img_gray.filter(ImageFilter.FIND_EDGES)
        return edges
