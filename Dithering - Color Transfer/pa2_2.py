"""
Color Transfer
"""

import cv2
import numpy as np


def rgb2lms(image):

    transformation_matrix = np.array([[0.3811, 0.5783, 0.0402],
                                      [0.1967, 0.7244, 0.0782],
                                      [0.0241, 0.1288, 0.8444]])
    # split the image channels
    b, g, r = cv2.split(image)

    l = transformation_matrix[0][0] * r + transformation_matrix[0][1] * g + transformation_matrix[0][2] * b
    m = transformation_matrix[1][0] * r + transformation_matrix[1][1] * g + transformation_matrix[1][2] * b
    s = transformation_matrix[2][0] * r + transformation_matrix[2][1] * g + transformation_matrix[2][2] * b

    return l, m, s


def check_log(elem):
    # check array item if it's 0, convert it to 1 to make log=0
    # it prevents divide by zero error
    result = np.where(elem == 0, 1, elem)
    return np.log10(result, out=result, where=result > 0)


def lms2lab(l, m, s):

    m1 = np.array([[1 / np.sqrt(3), 0, 0],
                   [0, 1 / np.sqrt(6), 0],
                   [0, 0, 1 / np.sqrt(2)]])
    m2 = np.array([[1, 1, 1],
                   [1, 1, -2],
                   [1, -1, 0]])
    t_matrix = np.dot(m1, m2)

    ll = t_matrix[0][0] * l + t_matrix[0][1] * m + t_matrix[0][2] * s
    a = t_matrix[1][0] * l + t_matrix[1][1] * m + t_matrix[1][2] * s
    b = t_matrix[2][0] * l + t_matrix[2][1] * m + t_matrix[2][2] * s

    return ll, a, b


def lab2lms(ll, a, b):

    m1 = np.array([[1, 1, 1],
                   [1, 1, -1],
                   [1, -2, 0]])
    m2 = np.array([[np.sqrt(3) / 3, 0, 0],
                   [0, np.sqrt(6) / 6, 0],
                   [0, 0, np.sqrt(2) / 2]])
    t_matrix = np.dot(m1, m2)

    l = t_matrix[0][0] * ll + t_matrix[0][1] * a + t_matrix[0][2] * b
    m = t_matrix[1][0] * ll + t_matrix[1][1] * a + t_matrix[1][2] * b
    s = t_matrix[2][0] * ll + t_matrix[2][1] * a + t_matrix[2][2] * b

    return l, m, s


def lms2rgb(l, m, s):

    transformation_matrix = np.array([[4.4679, -3.5873, 0.1193],
                                      [-1.2186, 2.3809, -0.1624],
                                      [0.0497, -0.2439, 1.2045]])

    r = transformation_matrix[0][0] * l + transformation_matrix[0][1] * m + transformation_matrix[0][2] * s
    g = transformation_matrix[1][0] * l + transformation_matrix[1][1] * m + transformation_matrix[1][2] * s
    b = transformation_matrix[2][0] * l + transformation_matrix[2][1] * m + transformation_matrix[2][2] * s

    r = np.clip(r, 0, 255)              # values should be scaled to get them in [0, 255] range
    g = np.clip(g, 0, 255)
    b = np.clip(b, 0, 255)

    new_image = cv2.merge((b, g, r))    # merge R, G, B channels to obtain the new image (cv2 uses BGR order !)
    new_image = np.uint8(new_image)

    return new_image


def colorTransfer(source, target):

    src_l, src_m, src_s = rgb2lms(source)
    target_l, target_m, target_s = rgb2lms(target)

    src_l, src_m, src_s = check_log(src_l), check_log(src_m), check_log(src_s)
    target_l, target_m, target_s = check_log(target_l), check_log(target_m), check_log(target_s)

    src_ll, src_a, src_b = lms2lab(src_l, src_m, src_s)
    target_ll, target_a, target_b = lms2lab(target_l, target_m, target_s)

    mean_ll_s, var_ll_s = np.mean(src_ll), np.var(src_ll)
    mean_a_s, var_a_s = np.mean(src_a), np.var(src_a)
    mean_b_s, var_b_s = np.mean(src_b), np.var(src_b)
    mean_ll_t, var_ll_t = np.mean(target_ll), np.var(target_ll)
    mean_a_t, var_a_t = np.mean(target_a), np.var(target_a)
    mean_b_t, var_b_t = np.mean(target_b), np.var(target_b)

    ll_star = src_ll - mean_ll_s                    # l*
    a_star = src_a - mean_a_s                       # a*
    b_star = src_b - mean_b_s                       # b*

    ll_prime = (var_ll_t / var_ll_s) * ll_star      # l'
    a_prime = (var_a_t / var_a_s) * a_star          # a'
    b_prime = (var_b_t / var_b_s) * b_star          # b'

    new_ll = ll_prime + mean_ll_t                   # l''
    new_a = a_prime + mean_a_t                      # a''
    new_b = b_prime + mean_b_t                      # b''

    l, m, s = lab2lms(new_ll, new_a, new_b)

    l_, m_, s_ = 10 ** l, 10 ** m, 10 ** s

    new_img = lms2rgb(l_, m_, s_)

    return new_img

