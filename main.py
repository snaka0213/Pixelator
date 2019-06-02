#!/usr/bin/env python3

import sys
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

# paint a part of `output` single color `pixel_color`
def draw_part_img(output, start_x, start_y, part_size_x, part_size_y, pixel_color):
    for y in range(start_y, start_y + part_size_y):
        for x in range(start_x, start_x + part_size_x):
            output.putpixel((x, y), pixel_color)

# return the means of color of `image_pixels`
def means_of_color(image_pixels):
    counter, sum = 0, 0
    for v in image_pixels:
        sum += np.sum(v, axis=0)
        counter += len(v)
    return tuple(int(x) for x in sum*(1/counter))

# input
## filter_size: the size of filters
## num_of_colors: the number of colors (=k)
## file_name: the name of input file
filter_size = int(input("Filter size? >> "))
num_of_colors = int(input("Number of colors? >> "))
file_name = input("File name? >> ")

try:
    img = Image.open(file_name)
except FileNotFoundError:
    print("File not found.")
    sys.exit()

# set `width`, `height`, `features`
## new_img: will be output
width, height = img.size
width, height = (width//filter_size) * filter_size, (height//filter_size) * filter_size
new_img = Image.new('RGB', (width, height))

features = []
img_pixels = np.array([[img.getpixel((x,y)) for x in range(width)] for y in range(height)])
for y in range(0, height, filter_size):
    for x in range(0, width, filter_size):
        part_img = img_pixels[y:y+filter_size, x:x+filter_size]
        features.append(means_of_color(part_img))

# k-means clustering
## centers: the representative colors of cluster
## labels: the labels of cluster
kmeans = KMeans(n_clusters=num_of_colors).fit(features)
centers = [tuple(int(x) for x in z) for z in kmeans.cluster_centers_]
labels = kmeans.labels_

# output
ind_y, ind_x = 0, 0
for y in range(0, height, filter_size):
    ind_x = 0
    for x in range(0, width, filter_size):
        part_img = img_pixels[y:y+filter_size, x:x+filter_size]
        pixel_color = centers[labels[ind_x + (ind_y*width)//filter_size]]
        draw_part_img(new_img, x, y, part_img.shape[1], part_img.shape[0], pixel_color)
        ind_x += 1
    ind_y += 1

# show and save output
new_img.show()
select = input("Save this file? [y/n] >> ")
if select != 'y':
    sys.exit()
else:
    new_file_name = input("New file name? >> ")
    new_img.save(new_file_name)
