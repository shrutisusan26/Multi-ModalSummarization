import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from extract import get_feat
import cv2


ip =r'E:\Multi-Modal Summarization\VideoSummarization\Data\videos\input.mp4'
fr = 4
get_feat(ip,fr)
opn =ip[0:10]
opn = opn.replace(r'\.','')
opn = opn.replace('\\','')
opn = opn.replace(':','')
output_file = './Data/'+opn+'op.npy'
print(output_file)
op = np.load(output_file)
print(op.shape)
n_clusters = op.shape[0]//8
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
cap = cv2.VideoCapture(ip)
fps = cap.get(cv2.CAP_PROP_FPS)
scale = fr*fps
for i in ordering:
    cap.set(1, i*scale)
    ret, frame = cap.read()
    fname=r'E:\Multi-Modal Summarization\VideoSummarization\Data\output_images\pic'+str(i)+".jpg"
    cv2.imwrite(fname, frame)