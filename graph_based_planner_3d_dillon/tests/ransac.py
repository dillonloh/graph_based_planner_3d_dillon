import numpy as np
import cv2
from matplotlib import pyplot as plt
from skimage import color, filters, exposure, morphology
import skimage

FLANN = False # if True, uses FLANN to match, else uses Brute Force
LOWES_CONSTANT = 0.7

MIN_MATCH_COUNT = 30

img1 = cv2.imread('./images/chinokyoten2f_marked.png', -1)          # queryImage
img2 = cv2.imread('./images/chinokyoten3f_marked.png', -1) # trainImage
img3 = cv2.imread('./images/chinokyoten1f_marked.png', -1)

img1 = skimage.color.rgb2gray(img1)
img2 = skimage.color.rgb2gray(img2)

# thresh = filters.threshold_otsu(img1)
# img1 = img1 > thresh

# thresh = filters.threshold_otsu(img2)
# img2 = img2 > thresh

img1 = img1.astype('uint8')
img2 = img2.astype('uint8')

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)    
kp2, des2 = sift.detectAndCompute(img2,None)


if FLANN == True:
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 300)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < LOWES_CONSTANT*n.distance:
            good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    else:
        print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
        matchesMask = None


    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    matchesMask = matchesMask, # draw only inliers
                    flags = 2,
                    matchesThickness = 3)

    imgoutput = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

    plt.imshow(imgoutput), plt.show()

    matches = flann.knnMatch(des1,des2,k=2)

else:
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < LOWES_CONSTANT*n.distance:
            good.append(m)

    # cv2.drawMatchesKnn expects list of lists as matches.
                
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0, maxIters=1000)
    matchesMask = mask.ravel().tolist()

    h, w = img1.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                   singlePointColor=None,
                   matchesMask=matchesMask,  # draw only inliers
                   flags=2)

    img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

    plt.imshow(img3),plt.show()
