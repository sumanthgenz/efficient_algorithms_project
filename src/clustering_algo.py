import random
import glob
from sklearn.cluster import KMeans
import numpy as np

from check import check_assignment

def map_rooms_to_plane(H, S):
	# Add your mapper function here @Will Shue.
	
	# return points, which is a (N, D) numpy array, where N is num_students, D is 3D coordinate
	# points have to be in the same order as student_1, student_2, ... student_N
	return points

def cluster_kmeans(points, N_samples):
	
	#has room assignments for k rooms, where k is in a range
	clusters = [] 
	
	#evaluate kmeans for k (num_clusters) in the range below:
	for k in range(int(0.25*N_samples), int(0.75*N_samples)):
		
		#labels shape is (N,)
		labels = KMeans(n_clusters = k, 
				n_init = 10,
				max_iter = 300,
				random_state=0,
				algorithm='auto'
		).fit(points)).labels_
		
		#append room assignment to clusters
		clusters.append([[i, labels[i]] for i in range(len(labels))])
		
	#clusters shape is (range(k), N)
	return clusters

def max_cluster(clusters):
	value = 0
	max_H = 0
	max_K = None
	
	for k in clusters:
		value = check_assignment(k):
		if value and value > max_H:
			max_H = value
			max_K = k
	return max_K

def main(H, S, N_samples):
	points = map_to_room(H, S)
	clusters = cluster_kmeans(points, N_samples)
	return max_cluster(clusters)

if __name__ == "__main__":
	H = None
	S = None
	N_samples = 10
	
	print(main(H, S, N_samples))



