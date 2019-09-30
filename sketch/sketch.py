import cv2 as cv
import numpy as np
import os
import imageio
import scipy.ndimage
import matplotlib.pyplot as plt

DIR_PATH = 'sketch\input'
SKETCH_PATH = 'sketch\output'

def dodge(front,back):
    result=front*255/(255-back) 
    result[result>255]=255
    result[back==255]=255
    return result.astype('uint8')

def grayscale(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

for file in os.listdir(DIR_PATH):
    file_path = os.path.join(DIR_PATH, file)
    print(file_path)
    s = imageio.imread(file_path)
    g=grayscale(s)
    i = 255-g
    b = scipy.ndimage.filters.gaussian_filter(i,sigma=10)
    r= dodge(b,g)
    plt.imshow(r, cmap="gray")    
    plt.imsave(os.path.join(SKETCH_PATH, file), r, cmap='gray', vmin=0, vmax=255)