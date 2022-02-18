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
import pandas as pd
import skimage.io

def get_frame(ip,fr,op):
    cap = cv2.VideoCapture(ip)
    fps = cap.get(cv2.CAP_PROP_FPS)
    scale = float(16*fps/fr)
    area_arr=[]
    run_avg = 0
    for i in range(len(op)):
        cap.set(1, i*scale)
        ret, frame = cap.read()
        if not ret:
            print("ERR")
        
        face_detector_op = face_detector(frame)
        if isinstance(face_detector_op,bool):
            continue
        area_arr.append(face_detector(frame))
        run_avg+=area_arr[i]
    run_avg = run_avg/len(area_arr)
    processed_frames = []
    frame_no=[]
    for i, vector in enumerate(op):
        if area_arr[i]!=True or area_arr[i]<=run_avg:
            processed_frames.append(vector)
            frame_no.append(i)
    print(len(op),len(processed_frames))
    return processed_frames,frame_no
    
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
            print(f"Removing {ordering[i]}")
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

def removeredundant(ordering,ip,fr):
    print(ip)
    cap = cv2.VideoCapture(ip)
    fps = cap.get(cv2.CAP_PROP_FPS)
    scale = float(16*fps/fr)
    lst =[]
    index = []
    for i in ordering:
        try:
            cap.set(1, i*scale)
            ret, frame = cap.read()
            if not ret:
                print("ERR")
            fname="pic.jpg"
            cv2.imwrite(fname, frame)
            image = skimage.io.imread('pic.jpg', as_gray=True)
            histogram, bin_edges = np.histogram(image, bins=256, range=(0, 1))
            lst.append(histogram)
        except Exception as e:
            print(e)
            print("no")
    a = np.array(lst)
    lst = (a.T).tolist()
    df = pd.DataFrame(lst)
    to_drop =[]
    corr_matrix = df.corr()
    for column in corr_matrix.columns:
        corr_matrix[column][column]=-1
        if all(corr_matrix[column] < 0.1):
            to_drop.append(column)
    for i in to_drop:
        ordering = [ordering[i] for i in range(len(ordering)) if i not in to_drop]
    return ordering

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
    output_file = opn+'op.npy'
    output_file = os.path.join(dir2,output_file)
    clean(dir1,output_file) 
    get_feat(ip,fr,output_file)
    op = np.load(output_file)
    preprocessed_frames,frame_no=get_frame(ip,fr,op)
    preprocessed_frames = np.array(preprocessed_frames)           
    n_clusters = getclusters(preprocessed_frames,n_clusters)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    print(len(preprocessed_frames))
    kmeans = kmeans.fit(preprocessed_frames)
    closest = []
    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_,preprocessed_frames)
    ordering = [frame_no[closest[idx].item()] for idx in range(n_clusters)]
    print(ordering)
    ordering = removeredundant(ordering,ip,fr)
    print(ordering)
    keyframes_vectors = [op[i] for i in ordering]
    print('Clustering Finished')
    np.save(output_file,keyframes_vectors)
    return ordering,fr,op.shape[0]

