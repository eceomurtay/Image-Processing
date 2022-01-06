import cv2
from pa2_2 import colorTransfer


def show_img(image):
    cv2.imshow("Color Transferred Image", image)
    cv2.waitKey()


if __name__ == '__main__':

    src_img = cv2.imread("./example images/colortransfer/storm.jpg")           # source image
    target_img = cv2.imread("./example images/colortransfer/woods.jpg")        # target palette

    color_transferred_img = colorTransfer(src_img, target_img)
    show_img(color_transferred_img)
