import cv2
import matplotlib.pyplot as plt
import numpy as np

from config import *

idx = 0

def get_rgb_and_semseg(idx):
    img_rgb = cv2.imread(DATA_DIR + f'images\\{idx}.png')
    img_gt = cv2.imread(DATA_DIR + f'labels\\{idx}.png', 0)

    img_gt_rgb = np.zeros((img_gt.shape[0], img_gt.shape[1], 3), np.uint8)

    for i in range(img_gt.shape[0]):
        for j in range(img_gt.shape[1]):
            img_gt_rgb[i, j, :] = id2label[img_gt[i, j]].color

    return img_rgb, img_gt_rgb


if __name__ == "__main__":
    DATA_DIR = 'C:\\data\\HmdSegmentation\\training\\'

    for i in range(6):
        img_rgb, img_gt_rgb = get_rgb_and_semseg(i)

        cv2.imshow('rgb', img_rgb)
        cv2.imshow('gt', img_gt_rgb)
        cv2.waitKey(500)
