import random
import glob
from sklearn.cluster import KMeans
import numpy as np

from checker import check_assignment, fill_matrix

def map_rooms_to_plane(H, S):
    # Add your mapper function here @Will Shue.
    
    # return points, which is a (N, D) numpy array, where N is num_students, D is 3D coordinate
    # points have to be in the same order as student_1, student_2, ... student_N

    def getD(i,j):
        return pow(S[i][j]/(H[i][j] + .01) + 5, 1/4)
    N = len(H)
    m = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            m[i][j] = 0.5*(((getD(1,i))**2) + ((getD(1,j))**2) - ((getD(i,j))**2))
    M = np.array(m)
    q, r = np.linalg.qr(A)
    b1 = q[:,0]
    b2 = q[:,1]
    points = []
    for i in range(N):
        points.append((np.dot(b1,M[:,i]),np.dot(b2,M[:,i])))
    return points

def cluster_kmeans(points, N_samples):
    #has room assignments for k rooms, where k is in a range
    clusters = [] 
    
    #represents assignment for a given value of k
    assignment = None
    lb = 0.0
    ub = 1.0
    if N_samples == 50:
        lb = 0.20
        ub = 0.75
    
    #evaluate kmeans for k (num_clusters) in the range below:
    for k in range(int(lb * N_samples) + 1, int(ub * N_samples)):
        
        assignment = [[]*k]
        
        #labels shape is (N,)
        kmean = KMeans(n_clusters = k, 
                n_init = 10,
                max_iter = 300,
                random_state=0,
                algorithm='auto'
        ).fit(points)
        labels = kmeans.labels_
        #append room assignment to clusters; WLOG formatted as (room, student_1, student_2...), (room2, student_5), ...
        for i in range(len(labels)):
            assignment[label[i]].append(i)
        clusters.append(assignment)
        
        #append room assignment to clusters; WLOG formatted as  (student_1, room), (student_2, room)...
        # clusters.append([[i, labels[i]] for i in range(len(labels))])
        
    #clusters shape is (range(k), N)
    return clusters

def max_cluster(clusters, N_samples):
    value = 0
    max_H = 0
    max_K = None
    
    for k in clusters:
        value = check_assignment(k, N_samples)
        if value and value > max_H:
            max_H = value
            max_K = k
    return max_K

def cluster_main(H, S, N_samples):
    points = map_rooms_to_plane(H, S)
    clusters = cluster_kmeans(points, N_samples)
    return max_cluster(clusters, N_samples)

if __name__ == "__main__":
    H = fill_matrix("data/inputs/small-31.in")
    S = None
    N_samples = 10
    
    print(cluster_main(H, S, N_samples))




