import cv2
import matplotlib.pyplot as plt
import numpy as np

from config import *

img_gt = cv2.imread('output/Image0076.png', 0)
img_rgb = cv2.imread('output/rgb/1.png')

plt.imshow(img_gt)

img_gt_rgb = np.zeros((img_gt.shape[0], img_gt.shape[1], 3), np.uint8)

for i in range(img_gt.shape[0]):
    for j in range(img_gt.shape[1]):
        img_gt_rgb[i, j, :] = id2label[img_gt[i, j]].color

cv2.imshow('t', img_rgb)
cv2.imshow('t', img_gt_rgb)
