import numpy as np
import cv2


def find_keypoints_homography(img1, img2):

    # initialize SIFT detector
    sift = cv2.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, desc1 = sift.detectAndCompute(img1, None)
    kp2, desc2 = sift.detectAndCompute(img2, None)

    # KD tree is used to find the most similar descriptor when performing the matching.
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    # match descriptors
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(desc1, desc2, k=2)     # 2-NN

    # Ratio test
    # good matches are considered as matches that distance between them is less than %70
    good = [m for m, n in matches if m.distance < 0.7 * n.distance]

    # computing homography requires at least 4 matches
    if len(good) > 4:

        # convert to numpy array from KeyPoint object
        im1_pts = np.array([kp1[m.queryIdx].pt for m in good])
        im2_pts = np.array([kp2[m.trainIdx].pt for m in good])

        src_pts = np.float32(im1_pts).reshape(-1, 1, 2)
        dst_pts = np.float32(im2_pts).reshape(-1, 1, 2)

        # findHomography() returns a mask which specifies the inlier and outlier points.
        h_matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        return h_matrix, im1_pts, im2_pts


def gaussian_pyramid(img, level):

    img_copy = img.copy()
    gaussian_pyr = [img_copy.astype('float32')]

    for i in range(level):

        # downsample the image
        img_copy = cv2.pyrDown(img_copy)
        gaussian_pyr.append(img_copy.astype('float32'))

    return gaussian_pyr


def laplacian_pyramid(img, level):

    g_pyr = gaussian_pyramid(img, level)
    laplacian_pyr = [g_pyr[level]]

    for i in range(level, 0, -1):

        size = (g_pyr[i - 1].shape[1], g_pyr[i - 1].shape[0])
        # upsample the image
        gaussian_upsampled = cv2.pyrUp(g_pyr[i]).astype('float32')
        gaussian_resized = cv2.resize(gaussian_upsampled, size)
        lap = np.subtract(g_pyr[i - 1], gaussian_resized)
        laplacian_pyr.append(lap)

    return laplacian_pyr


def warping(imgm, imgr, imgl):

    # expand the image size by adding border
    imgm = cv2.copyMakeBorder(imgm, 200, 200, 500, 500, cv2.BORDER_CONSTANT)

    # Right + Middle
    m_rm, pt_rm1, pt_rm2 = find_keypoints_homography(imgr, imgm)
    warped_right = cv2.warpPerspective(imgr, m_rm,
                                       (imgm.shape[1], imgm.shape[0]),
                                       dst=imgm.copy(),
                                       borderMode=cv2.BORDER_TRANSPARENT)

    # Left + Middle
    m_lm, pt_lm1, pt_lm2 = find_keypoints_homography(imgl, imgm)
    warped_left = cv2.warpPerspective(imgl, m_lm,
                                      (imgm.shape[1], imgm.shape[0]),
                                      dst=imgm.copy(),
                                      borderMode=cv2.BORDER_TRANSPARENT)

    return warped_left, warped_right


def blending(w1, w2, level):

    # Laplacian pyramid for LM
    pyr1 = laplacian_pyramid(w1, level)
    # Laplacian pyramid for RM
    pyr2 = laplacian_pyramid(w2, level)

    pyramid = []

    for lap1, lap2 in zip(pyr1, pyr2):

        row, col, _ = lap1.shape
        mask1 = np.zeros(lap1.shape)
        mask2 = np.zeros(lap2.shape)
        mask1[:, 0:col // 2, :] = 1
        mask2[:, col // 2:, :] = 1

        laplacian1 = np.multiply(lap1, mask1.astype('float32'))
        laplacian2 = np.multiply(lap2, mask2.astype('float32'))

        laplacian = np.add(laplacian1, laplacian2)
        pyramid.append(laplacian)

    # reconstruct
    result = pyramid[0]

    for i in range(1, level + 1):

        size = (pyramid[i].shape[1], pyramid[i].shape[0])
        result = cv2.pyrUp(result)
        result = cv2.resize(result, size)
        result = np.add(result, pyramid[i])

    # to get the values in 0-255 range
    np.clip(result, 0, 255, out=result)
    return result.astype('uint8')


if __name__ == '__main__':

    img_left = cv2.imread('./building1.jpg')
    img_middle = cv2.imread('./building2.jpg')
    img_right = cv2.imread('./building3.jpg')

    warped1, warped2 = warping(img_middle, img_right, img_left)
    panorama = blending(warped1, warped2, 5)

    # Crop the black pixels around the panoramic image
    gray = cv2.cvtColor(panorama, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = panorama[y:y + h, x:x + w]

    cv2.imshow("Panorama", crop)
    cv2.waitKey(0)

