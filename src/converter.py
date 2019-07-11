#!/usr/bin/env python3
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

class DotConverter(object):
    def __init__(self, filter_size: int, colors: int, image=None):
        self._filter = filter_size # the length of filter square's side
        self._colors = colors # the number of colors
        self._image = image # input image: Image.Image

    # input image
    def load(self, path: str):
        self._image = Image.open(path)

    # show image
    def show(self):
        image = self._image
        if image:
            image.show()

    # save image
    def save(self, path: str):
        image = self._image
        if image:
            image.save(path)

    # mosaic processing
    ## if change, do mosaic proccessing on `self._image`
    ## return features list, which is stored in order like this:
    ## [begin ->  ... ]
    ## ...
    ## [ ...  ->  end ]
    def pixelate(self, change=False) -> list:
        image = self._image
        if image:
            features = []

            filter_size = self._filter
            width, height = self.get_size_rescaled(image.size)
            pixels_matrix = self.get_pixels_matrix(width, height)
            if change:
                self._image = Image.new('RGB', (width, height))

            for y in range(0, height, filter_size):
                for x in range(0, width, filter_size):
                    part_img = pixels_matrix[y:y+filter_size, x:x+filter_size]
                    single_color = self._means_of_color(part_img)
                    features.append(single_color)
                    if change:
                        self._draw_part_img(x, y, filter_size, filter_size, single_color)

            return features

    # retro game picture converter
    def convert(self):
        filter_size = self._filter
        image = self._image
        if image:
            width, height = self.get_size_rescaled(image.size)

            features = self.pixelate()
            k_means = self.k_means_clustering(features)
            centers, labels = k_means["centers"], k_means["labels"]

            self._image = Image.new('RGB', (width, height))
            ind_y, ind_x = 0, 0
            for y in range(0, height, filter_size):
                ind_x = 0
                for x in range(0, width, filter_size):
                    pixel_color = centers[labels[ind_x + (ind_y*width)//filter_size]]
                    self._draw_part_img(x, y, filter_size, filter_size, pixel_color)
                    ind_x += 1
                ind_y += 1

    # k-means clustering
    ## centers: the representative colors of cluster
    ## labels: the labels of cluster
    def k_means_clustering(self, features: list) -> dict:
        # TODO: make it does not change `features`
        kmeans = KMeans(n_clusters=self._colors).fit(features)
        centers = [tuple(int(x) for x in z) for z in kmeans.cluster_centers_]
        labels = kmeans.labels_
        return {"centers": centers, "labels": labels}

    # return np.ndarray of pixels of image
    ## [p_11 p_12 ... p_1w] (w = width, h = height)
    ## [p_21 p_22 ... p_2w]
    ## ...
    ## [p_h1 p_h2 ... p_hw]
    def get_pixels_matrix(self, width: int, height: int) -> np.ndarray:
        image = self._image
        _pixels_list = [[image.getpixel((x, y)) for x in range(width)] for y in range(height)]
        return np.array(_pixels_list)

    # return rescaled size which is multiple of filter size
    def get_size_rescaled(self, size: tuple) -> tuple:
        filter_size = self._filter
        return tuple([(side//filter_size)*filter_size for side in size])

    # paint a part of self with `single_color`
    def _draw_part_img(self, start_w, start_h, part_size_w, part_size_h, single_color):
        for y in range(start_h, start_h + part_size_h):
            for x in range(start_w, start_w + part_size_w):
                self._image.putpixel((x, y), single_color)

    # return the means of color of `pixels_matrix`:
    def _means_of_color(self, pixels_matrix: np.ndarray) -> tuple:
        counter, sum = 0, 0
        for v in pixels_matrix:
            sum += np.sum(v, axis=0)
            counter += len(v)
        return tuple(int(x) for x in sum*(1/counter))
