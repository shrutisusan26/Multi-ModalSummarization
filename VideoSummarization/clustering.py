import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

op = np.load('op.npy')
print(op.shape)
n_clusters = int(op.shape[0]//3)
print(n_clusters)
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
kmeans = kmeans.fit(op)
avg = []
closest = []
for j in range(n_clusters):
    idx = np.where(kmeans.labels_ == j)[0]
    avg.append(np.mean(idx))
closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_,op)
clustering_ordering = sorted(range(n_clusters), key=lambda k: avg[k])
ordering = [closest[idx].item() for idx in clustering_ordering]
print('Clustering Finished')  
print(ordering)