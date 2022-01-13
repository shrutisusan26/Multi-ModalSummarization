from typing import OrderedDict
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import scipy
from VideoSummarization.extract import get_feat
import cv2
import os 

def cosine_distance_between_two_images(v1, v2):
    return (1- scipy.spatial.distance.cosine(v1, v2))

def getfr(ip):
    stream = cv2.VideoCapture(ip)
    fps = stream.get(cv2.CAP_PROP_FPS)  
    frame_count = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))
    dur = frame_count/fps
    lt = [24,20,16,12,8,4]
    i = 0
    while i < len(lt) and dur * lt[i] > 14000:
        i = i+1
    if i < len(lt):
        return lt[i]
    else:
        return lt[-1]
def redundancy_checker(ordering,op):
    final_list=ordering.copy()
    for i in range(len(ordering)-1):
        if cosine_distance_between_two_images(op[ordering[i]],op[ordering[i+1]]) > 0.95:
            final_list.remove(ordering[i])
    return final_list
        
def clean(dir1,dir2,op):
    if os.path.isfile(op):
        os.remove(op)
    for j in [dir1,dir2]:
        print(j)
        arr = os.listdir(j)
        if arr:
            for i in arr:
                print(j+"\\"+i)
                #os.remove(j+"\\"+i)
                os.remove(os.path.join(j,i))

def vsum(ip):
    dir1 = os.path.join(os.getcwd(),'Data')
    dir1 = os.path.join(dir1,'output_images')
    dir2 = os.path.join(os.getcwd(),'Data')
    dir2 = os.path.join(dir2,'red')
    if not os.path.isdir(dir1):
        os.makedirs(dir1)
    if not os.path.isdir(dir2):
        os.makedirs(dir2)
    fr = getfr(ip)
    opn =ip[0:10]
    opn = opn.replace(r'\.','')
    opn = opn.replace('\\','')
    opn = opn.replace(':','')
    opf = os.path.join(os.getcwd(),'Data')
    output_file = opn+'op.npy'
    output_file = os.path.join(opf,output_file)
    clean(dir1,dir2,output_file) 
    get_feat(ip,fr)
    print(output_file)
    op = np.load(output_file)
    print(op.shape)
    n_clusters = max(5,op.shape[0]//10)
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
    removed_redundancy = redundancy_checker(ordering,op)
    print('Clustering Finished')
    cap = cv2.VideoCapture(ip)
    fps = cap.get(cv2.CAP_PROP_FPS)
    scale = (16/fr)*fps
    # for i in ordering:
    #     cap.set(1, i*scale)
    #     ret, frame = cap.read()
    #     fname=r'E:\Multi-Modal Summarization\VideoSummarization\Data\output_images\pic'+str(i)+".jpg"
    #     cv2.imwrite(fname, frame)

    # for i in removed_redundancy:
    #     cap.set(1, i*scale)
    #     ret, frame = cap.read()
    #     fname=r'E:\Multi-Modal Summarization\VideoSummarization\Data\red\pic'+str(i)+".jpg"
    #     cv2.imwrite(fname, frame)
    return ordering,fr

