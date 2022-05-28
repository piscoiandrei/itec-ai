import os
import shutil
import cv2
import numpy as np
import multiprocessing as mp
from PIL import Image

from utils.settings import TOTAL_AREA


def init():
    try:
        shutil.rmtree('kmean_img')
    except OSError:
        pass
    try:
        os.mkdir('kmean_img')
    except OSError:
        pass


def get_color_and_area(img):
    counter = {}
    for row in img:
        for pixel in row:
            key = " ".join([str(p) for p in pixel])
            if key in counter:
                counter[key] += 1
            else:
                counter[key] = 1
    colors_rgb = []
    for key in counter.keys():
        colors_rgb.append([int(x) for x in key.split(' ')])
    mx_color_pixel = colors_rgb[0] if max(colors_rgb[0]) > max(
        colors_rgb[1]) else colors_rgb[1]
    colors = ["red", "green", "blue"]
    return colors[mx_color_pixel.index(max(mx_color_pixel))], counter[" ".join(
        [str(p) for p in mx_color_pixel]
    )] / TOTAL_AREA


def compute_kmeans(path):
    init()
    image = cv2.imread(f'images/{path}')
    # convert to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = image.reshape((-1, 3))
    # convert to float
    pixel_values = np.float32(pixel_values)
    # define stopping criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.2)
    # number of clusters (K)
    k = 2
    _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10,
                                      cv2.KMEANS_RANDOM_CENTERS)
    # convert back to 8 bit values
    centers = np.uint8(centers)
    # flatten the labels array
    labels = labels.flatten()
    # convert all pixels to the color of the centroids
    segmented_image = centers[labels.flatten()]
    # reshape back to the original image dimension
    segmented_image = segmented_image.reshape(image.shape)
    color, area = get_color_and_area(segmented_image)
    return ",".join(str(x) for x in [path, color, area])


def kmeans_range(final_data, paths):
    data = []
    for p in paths:
        data.append(compute_kmeans(p))
    final_data.append(data)


def kmean_processes():
    manager = mp.Manager()
    final_data = manager.list()
    paths = files = os.listdir('images/')
    processes = []
    for i in range(0, len(paths), 100):
        proc = mp.Process(target=kmeans_range,
                          args=(final_data, paths[i:i + 100],))
        processes.append(proc)
        proc.start()
    for p in processes:
        p.join()
    final_data = [s for sublist in final_data for s in sublist]
    with open('kmean_out.txt', 'w') as f:
        for x in final_data:
            f.writelines(x + "\n")
