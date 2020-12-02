import random
import glob
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import math
import tqdm

from checker import check_assignment, fill_matrix

def map_rooms_to_plane(H, S, path):
    # Add your mapper function here @Will Shue.
    
    # return points, which is a (N, D) numpy array, where N is num_students, D is 3D coordinate
    # points have to be in the same order as student_1, student_2, ... student_N

    def getD(i,j):
        return pow(S[i][j]/(H[i][j] + 0.01) + 5, 1/4)
        # return (S[i][j]) / ((H[i][j]) + .1)


    N = len(H)
    m = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            m[i][j] = 0.5*(((getD(1,i))**2) + ((getD(1,j))**2) - ((getD(i,j))**2))
    M = np.array(m)
    q, r = np.linalg.qr(M)
    b1 = q[:,0]
    b2 = q[:,1]
    points = []
    for i in range(N):
        points.append((np.dot(b1,M[:,i]),np.dot(b2,M[:,i])))
    # x, y = zip(*points)
    # fig = plt.figure()
    # ax = fig.add_subplot()
    # ax.scatter(x, y)
    # plt.savefig("data/input_clusters/{}.png".format(path))
    return points

def cluster_kmeans(points, N_samples):
    #has room assignments for k rooms, where k is in a range
    clusters = [] 
    
    #represents assignment for a given value of k
    assignment = None
    lb = 0.1
    ub = 1.0
    # if N_samples == 50:
    #     lb = 0.20
    #     ub = 0.75
    
    #evaluate kmeans for k (num_clusters) in the range below:
    for k in range(int(lb * N_samples), int(ub * N_samples)+1):
        
        assignment = {}
        #labels shape is (N,)
        kmeans = KMeans(n_clusters = k, 
                n_init = 10,
                max_iter = 300,
                random_state=0,
                algorithm='auto'
        ).fit(points)
        labels = kmeans.labels_
        #append room assignment to clusters; WLOG formatted as (room, student_1, student_2...), (room2, student_5), ...
        for i in range(len(labels)):
            if labels[i] not in assignment:
                assignment[labels[i]] = []
            assignment[labels[i]].append(i)
        cluster = [assignment[key] for key in list(assignment.keys())]
        clusters.append(cluster)
        
        #append room assignment to clusters; WLOG formatted as  (student_1, room), (student_2, room)...
        # clusters.append([[i, labels[i]] for i in range(len(labels))])
        
    #clusters shape is (range(k), N)
    return clusters

def max_cluster(clusters, N_samples, s_max, H, S):
    value = 0
    max_H = 0
    max_K = None
    
    for clust in clusters:
        value = check_assignment(clust, s_max, N_samples, H, S)
        if value and value > max_H:
            max_H = value
            max_K = clust
    return max_K, max_H

def cluster_main(H, S, N_samples, s_max):
    points = map_rooms_to_plane(H, S)
    clusters = cluster_kmeans(points, N_samples)
    return max_cluster(clusters, N_samples, s_max, H, S)

if __name__ == "__main__":

    for path in glob.glob('data/inputs/*'): 
        H, S, n_students, s_max = fill_matrix(path)
        # points = map_rooms_to_plane(H, S, path.split("/")[-1][:-3])
        print(cluster_main(H, S, n_students, s_max))




