import shutil
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import scipy
from VideoSummarization.extract import get_feat
import cv2
import os 
import shutil
from helper import dirgetcheck, getclusters
import re
from VideoSummarization.face_detector import face_detector

def get_frame(ip,fr,frame_num):
    cap = cv2.VideoCapture(ip)
    fps = cap.get(cv2.CAP_PROP_FPS)
    scale = float(16*fps/fr)


    try:
        cap.set(1, frame_num*scale)
        ret, frame = cap.read()
        if not ret:
            print("ERR")
        return face_detector(frame,0.05)
    except:
        print("Face Detection gone wrong")
def cosine_distance_between_two_images(v1, v2):
    """
    Calculates cosine similarity between 2 vectors.

    Args:
        v1 (np arr): Vector corresponding to a frame.
        v2 (np arr): Vector corresponding to a frame.

    Returns:
        int: Cosine similarty between the 2 vectors.
    """
    return (1- scipy.spatial.distance.cosine(v1, v2))

def getfr(ip):
    """
    Function to calculate processing framerate with respect to memory 
    limitatons.

    Args:
        ip (str): File path.

    Returns:
        int: Frame rate.
    """
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
    """
    Function to detect redundant images out of all the keyframes.
    Works on cosine similarity.

    Args:
        ordering (list): List containing indexes of keyframes.
        op (np app): Numpy arr containing features of all the frames.

    Returns:
        final_list (list): List containg indexes of rendundancy removed keyframes.
    """
    final_list=ordering.copy()
    for i in range(len(ordering)-1):
        if cosine_distance_between_two_images(op[ordering[i]],op[ordering[i+1]]) > 0.95:
            final_list.remove(ordering[i])
    return final_list
        
def clean(dir1,op):
    """
    Function to remove a particular file and all the files from a directory. 

    Args:
        dir1 (str): Path to directory.
        op (str): Path to file.
    """
    if os.path.isfile(op):
        os.remove(op)
    shutil.rmtree(dir1)
    os.makedirs(dir1)

def vsum(ip,n_clusters):
    """
    Function to calculate and return keyframes.

    Args:
        ip (str): File path.
        n_clusters (int): Baseline value of number of clusters to find optimum number.
        of keyframes.

    Returns:
        ordering,fr,op.shape[0] (list,int,int): List containing indexes of keyframes, processing 
        frame rate, number of chunks of size 16 in the entire video.
    """
    dir1 = dirgetcheck('Data','output_images')
    dir2 = dirgetcheck('Data','feat_op')
    fr = getfr(ip)
    opn = ip.split("\\")[-1].split('.')[0]
    opn=re.sub(r'[.\:]','',opn)
    # opn = opn.replace(r'\.','')
    # opn = opn.replace('\\','')
    # opn = opn.replace(':','')
    output_file = opn+'op.npy'
    output_file = os.path.join(dir2,output_file)
    clean(dir1,output_file) 
    get_feat(ip,fr,output_file)
    op = np.load(output_file)
    
    preprocessed_frames = []
    frame_no = []
    
    for i, vector in enumerate(op):
        if not get_frame(ip,fr,i):
            preprocessed_frames.append(vector)
            frame_no.append(i)
            
    n_clusters = getclusters(preprocessed_frames,n_clusters)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans = kmeans.fit(op)
    closest = []
    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_,preprocessed_frames)
    print(closest)
    ordering = [frame_no[closest[idx].item()] for idx in range(n_clusters)]
    keyframes_vectors = [op[i] for i in ordering]
    print('Clustering Finished')
    np.save(output_file,keyframes_vectors)
    return ordering,fr,op.shape[0]

