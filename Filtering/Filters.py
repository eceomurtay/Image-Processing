import cv2
import numpy as np


class Filtering:

    def __init__(self, image, filter_size):

        self.image = image
        self.filter_size = filter_size

        # 3x3 filter
        self.three_filter = np.ones([3, 3]) * (1 / 9)
        # 5x5 filter
        self.five_filter = np.ones([5, 5]) * (1 / 25)
        # 7x7 filter
        self.seven_filter = np.ones([7, 7]) * (1 / 49)
        # 9x9 filter
        self.nine_filter = np.ones([9, 9]) * (1 / 81)

    def padding(self, img):         # add border around the image by reflecting edge pixels

        if self.filter_size == 3:
            padded = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_REFLECT)
        elif self.filter_size == 5:
            padded = cv2.copyMakeBorder(img, 2, 2, 2, 2, cv2.BORDER_REFLECT)
        elif self.filter_size == 7:
            padded = cv2.copyMakeBorder(img, 3, 3, 3, 3, cv2.BORDER_REFLECT)
        elif self.filter_size == 9:
            padded = cv2.copyMakeBorder(img, 4, 4, 4, 4, cv2.BORDER_REFLECT)

        return padded

    def mean_filter(self, padded, kernel):

        output = np.copy(self.image)
        # expand the filter's dimension (add 3rd channel)
        kernel = np.repeat(np.expand_dims(kernel, axis=-1), self.image.shape[-1], axis=-1)

        # iterate on image using padded image
        for i in range(padded.shape[0] - self.filter_size + 1):
            for j in range(padded.shape[1] - self.filter_size + 1):
                window = padded[i:i + self.filter_size, j:j + self.filter_size]
                # mean is calculated before -> x * 1/9 .. therefore, sum operator is used
                new_pixel = np.sum(window * kernel, axis=(0, 1))
                output[i][j] = new_pixel

        return output

    def gaussian_kernel(self, sigma):       # creates the Gaussian kernel

        x, y = np.mgrid[-self.filter_size // 2 + 1: self.filter_size // 2 + 1,
                        -self.filter_size // 2 + 1: self.filter_size // 2 + 1]
        g = np.exp(-((x ** 2 + y ** 2) / (2.0 * sigma ** 2)))
        return g / g.sum()

    def gaussian_filter(self, padded, kernel):

        output = np.copy(self.image)
        # expand the filter's dimension (add 3rd channel)
        kernel = np.repeat(np.expand_dims(kernel, axis=-1), self.image.shape[-1], axis=-1)

        # iterate on image using padded image
        for i in range(padded.shape[0] - self.filter_size + 1):
            for j in range(padded.shape[1] - self.filter_size + 1):
                window = padded[i:i + self.filter_size, j:j + self.filter_size]
                new_pixel = np.sum(window * kernel, axis=(0, 1))                    # element wise multiplication
                output[i][j] = new_pixel

        return output

    @staticmethod
    def find_min(q1, q2, q3, q4):

        std_q1 = np.std(q1)
        std_q2 = np.std(q2)
        std_q3 = np.std(q3)
        std_q4 = np.std(q4)

        # returns the index of min
        return np.argmin([std_q1, std_q2, std_q3, std_q4])

    @staticmethod
    def calculate_mean(idx, image, h, w, rad):

        if idx == 0:                    # Q1
            b = np.mean(image[h:h + rad + 1, w:w + rad + 1, 0])
            g = np.mean(image[h:h + rad + 1, w:w + rad + 1, 1])
            r = np.mean(image[h:h + rad + 1, w:w + rad + 1, 2])
        elif idx == 1:                  # Q2
            b = np.mean(image[h:h + rad + 1, w + rad:w + rad + rad + 1, 0])
            g = np.mean(image[h:h + rad + 1, w + rad:w + rad + rad + 1, 1])
            r = np.mean(image[h:h + rad + 1, w + rad:w + rad + rad + 1, 2])
        elif idx == 2:                  # Q3
            b = np.mean(image[h + rad:h + rad + rad + 1, w:w + rad + 1, 0])
            g = np.mean(image[h + rad:h + rad + rad + 1, w:w + rad + 1, 1])
            r = np.mean(image[h + rad:h + rad + rad + 1, w:w + rad + 1, 2])
        elif idx == 3:                  # Q4
            b = np.mean(image[h + rad:h + rad + rad + 1, w + rad:w + rad + rad + 1, 0])
            g = np.mean(image[h + rad:h + rad + rad + 1, w + rad:w + rad + rad + 1, 1])
            r = np.mean(image[h + rad:h + rad + rad + 1, w + rad:w + rad + rad + 1, 2])

        return b, g, r

    def kuwahara_filter(self, rgb_padded, _v):

        output = np.copy(self.image)
        height, weight, _ = self.image.shape
        radius = self.filter_size // 2                  # radius is the size of each quadrant

        # iterate on rgb image
        for h in range(height):
            for w in range(weight):
                window = _v[h: h + self.filter_size, w: w + self.filter_size]           # extract the window from V
                # divide the window into 4 equal sized subregions
                _Q1 = window[0: radius + 1, 0: radius + 1]
                _Q2 = window[0: radius + 1, radius: radius + radius + 1]
                _Q3 = window[radius: radius + radius + 1, 0: radius + 1]
                _Q4 = window[radius: radius + radius + 1, radius: radius + radius + 1]

                q_idx = self.find_min(_Q1, _Q2, _Q3, _Q4)                         # find the region that has min std dev

                new_pixel = self.calculate_mean(q_idx, rgb_padded, h, w, radius)   # get mean of each channel separately

                output[h][w][0] = new_pixel[0]
                output[h][w][1] = new_pixel[1]
                output[h][w][2] = new_pixel[2]

        return output


if __name__ == '__main__':

    rgb_img = cv2.imread("./france.jpg")  # read image
    rgb_img = cv2.resize(rgb_img, (int(rgb_img.shape[1] * 1 / 2), int(rgb_img.shape[0] * 1 / 2)))  # resize image by 1/2

    f = Filtering(rgb_img, 9)
    padded_img = f.padding(rgb_img)
    """
    # Kuwahara Filter

    padded_hsv = f.padding(cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV))            # hsv img is also padded
    v = padded_hsv[:, :, 2]                                                     # take V component only
    kuwahara_filtered = f.kuwahara_filter(padded_img, v)

    # cv2.imwrite("5x5 Kuwahara Filtered Image.jpg", kuwahara_filtered)"""
    """
    Q1 | Q2
    -------
    Q3 | Q4
    """
    """
    # Mean Filter
    
    mean_filtered = f.mean_filter(padded_img, f.nine_filter)                # filter should be changed according to size
    # cv2.imwrite("5x5 " + "Mean Filtered Image.jpg", mean_filtered)
    """

    # Gaussian Filter
    
    g_kernel = f.gaussian_kernel(sigma=1)
    gaussian_filtered = f.gaussian_filter(padded_img, g_kernel)             # create Gaussian kernel according to size
    # cv2.imwrite("5x5 sig_1 Gaussian Filtered Image.jpg", gaussian_filtered)


