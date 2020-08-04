# -*- coding: utf-8 -*-

import cv2
import numpy as np

# dummy function for mandatory trackbar callback
def dummy(value):
    pass

# define convolution kernels
identity_kernal = np.matrix('0 0 0; 0 1 0; 0 0 0')
sharpen_kernel = np.matrix('0, -1, 0; -1 5 -1; 0 -1 0')
gaussian_kernel1 = cv2.getGaussianKernel(3, 0)
gaussian_kernel2 = cv2.getGaussianKernel(11, 0)
box_kernel = np.ones([3, 3], np.float32) / 9.0
custom_kernel1 = np.matrix('2 1 0; 1 0 -1; 0 -1 -2')
custom_kernel2 = np.matrix('-1 -1 -1, -1 8 -1, -1 -1 -1')
custom_kernel3 = np.matrix('-3 5 5; -3 0 5; -3 -3 -3')

kernels = [identity_kernal, sharpen_kernel, gaussian_kernel1, gaussian_kernel2, 
           box_kernel, custom_kernel1, custom_kernel2, custom_kernel3]

# read in image and make greyscale copy
image = cv2.imread('wp1897910.jpg')
color_original = cv2.resize(image, (0,0), fx=0.7, fy=0.7)
grey_original = cv2.cvtColor(color_original, cv2.COLOR_BGR2GRAY)

# create the UI (window and trackbars)
cv2.namedWindow('app')
# arguements: trackbarName, windowName, value, count, onChange
cv2.createTrackbar('Greyscale', 'app', 0, 1, dummy)
cv2.createTrackbar('Filter', 'app', 0, len(kernels) - 1, dummy)
cv2.createTrackbar('Brightness', 'app', 100, 200, dummy)
cv2.createTrackbar('Contrast', 'app', 1, 25, dummy)

count = 1

#main UI loop
while True:
    greyscale = cv2.getTrackbarPos('Greyscale', 'app')
    kernel_idx = cv2.getTrackbarPos('Filter', 'app')
    brightness = cv2.getTrackbarPos('Brightness', 'app')
    contrast = cv2.getTrackbarPos('Contrast', 'app')
    
    # apply filters
    color_modified = cv2.filter2D(color_original, -1, kernels[kernel_idx])
    grey_modified = cv2.filter2D(grey_original, -1, kernels[kernel_idx])
    
    # apply brightness and contrast
    color_modified = cv2.addWeighted(color_modified, contrast, np.zeros_like(color_original), 0, brightness - 100)
    grey_modified = cv2.addWeighted(grey_modified, contrast, np.zeros_like(grey_original), 0, brightness - 100)
    
    key = cv2.waitKey(100)
    if key == ord('q'):
        break
    elif key == ord('s'):
        # save image
        if greyscale == 0:
            cv2.imwrite('output-{}.png'.format(count), color_modified)
        else:
            cv2.imwrite('output-{}.png'.format(count), grey_modified)
        count += 1
        
    if greyscale == 0:
        cv2.imshow('app', color_modified)
    else:
        cv2.imshow('app', grey_modified)

# window cleanup
cv2.destroyAllWindows()