import cv2 as cv
import numpy as np

depth_map = np.genfromtxt("depth_map.csv", delimiter=",")
print(depth_map.shape)
np.nan_to_num(depth_map, nan=0.0, posinf=0.0)
