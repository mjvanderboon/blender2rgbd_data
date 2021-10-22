import cv2
import matplotlib.pyplot as plt
import numpy as np

from config import *

idx = 0

def get_rgb_and_semseg(idx):
    img_gt = cv2.imread(f'output/gt/{idx}.png', 0)
    img_rgb = cv2.imread(f'output/rgb/{idx}.png')

    img_gt_rgb = np.zeros((img_gt.shape[0], img_gt.shape[1], 3), np.uint8)

    for i in range(img_gt.shape[0]):
        for j in range(img_gt.shape[1]):
            img_gt_rgb[i, j, :] = id2label[img_gt[i, j]].color

    return img_rgb, img_gt_rgb


if __name__ == "__main__":
    for i in range(20):
        img_rgb, img_gt_rgb = get_rgb_and_semseg(i)

        cv2.imshow('rgb', img_rgb)
        cv2.imshow('gt', img_gt_rgb)
        cv2.waitKey(10)
