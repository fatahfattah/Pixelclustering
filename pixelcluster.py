
import random
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from os import pardir
from dataloader import load_input
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-image', help='Provide input image', required=False)
    args = parser.parse_args()

    image = args.image if args.image else "examples/example_image.tif"

    image = Image.open(image)
    image = image.resize((150, 150))
    image = image.convert("L")
    image = np.array(image)
    m = len(image)
    n = len(image[0])

    mat = []
    
    for i in range(m):
        mat.append(['o' if image[i][j] < 220 else 'x' for j in range(len(image[i]))])

    # print(mat)
    def expand(cluster_id, clusters, i, j, mat, k=3, pixels=None):
        if i > 0 and j > 0 and i < len(mat) and j < len(mat[0]):
            if mat[i][j] == 'o':
                clusters[cluster_id].append((i, j))
                mat[i][j] = '@'
                for d in range(i-k, i+k):
                    for l in range(j-k, j+k):
                        expand(cluster_id, clusters, d, l, mat, k, pixels)
            
    # print(mat)
    clusters = {}
    pixels = []
    for i in range(m):
        for j in range(len(mat[0])):
            # print(image[i][j])
            if mat[i][j] == 'o':
                cluster_id = len(clusters.keys())
                clusters[cluster_id] = [(i, j)]
                expand(cluster_id, clusters, i, j, mat, k=5, pixels=pixels)

    size_threshold = 100
    clusters = dict(filter(lambda x: len(x[1]) >= size_threshold, clusters.items()))
    print(f"n: {len(clusters.keys())}")
    for cluster_id, coords in clusters.items():
        print(f"id: {cluster_id}, size: {len(coords)}")

    plt.imshow(image)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    for cluster_id, coords in clusters.items():
        for i, j in coords:
            plt.scatter(j, i, c= colors[cluster_id%len(colors)])

    plt.show()