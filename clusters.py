from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt
import numpy as np
import random

num_points = 50
helix_points = 100
num_centroids = 10

x_var = 3
y_var = 3
z_var = 3

def generate_cluster(n_points, x1, x2, y1, y2, z1, z2):
    x = x2 + (x1-x2)*np.random.rand(n_points)
    y = y2 + (y1-y2)*np.random.rand(n_points)
    z = z2 + (z1-z2)*np.random.rand(n_points) 
    return x, y, z

def generate_gaussian_centroids():
    x_c, y_c, z_c = generate_points(10, -sz, sz, -sz, sz, -sz, sz)
    centroids = [[x, y, z] for x, y, z in zip( x_c, y_c, z_c)]
    return centroids

def generate_helical_centroids():
    stride = helix_points//num_centroids
    angle = np.linspace(0, 4 * np.pi, helix_points)
    x_c = theta*25
    z_c =  np.sin(angle)*20
    y_c =  np.cos(angle)*5
    x_c, y_c, z_c = x_c[::5][:10], y_c[::5][:10], z_c[::5][:10]
    centroids = [[x, y, z] for x, y, z in zip( x_c, y_c, z_c)]
    return centroids

def generate_gaussian_mixture(centroids):
    clustered_points = []
    for centroid in centroids:
        x, y, z = centroid
        xs, ys, zs = generate_cluster(4, 
                                     x-x_var, x+x_var, 
                                     y-y_var, y+y_var, 
                                     z-z_var, z+z_var)
        ax.scatter(xs, ys, zs, marker="^")
        points = [[x, y, z] for x, y, z in zip(xs, ys, zs)]
        clustered_points += [centroid]
        for p in points:
            clustered_points += [p]
    return clustered_points
    
def visualize_clusters(points):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        xs, ys, zs = zip(*points)
        ax.scatter(xs, ys, zs)

    
if __name__=="__main__":
#     centroids = generate_gaussian_centroids()
    centroids = generate_helical_centroids()
    points = generate_gaussian_mixture(centroids)
    visualize_clusters(points)
    assert(len(points)==num_points)
    return points
