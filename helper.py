import os
import numpy as np
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from gap_statistic import OptimalK


class OptimalClusters:
    def __init__(self, data, min_clusters, max_clusters):
        self.data = data
        self.min_clusters = min_clusters
        self.max_clusters = max_clusters
        self.model = KMeans()
        
    def gap_statistic(self, nrefs=5):
        optimalK = OptimalK(parallel_backend='rust')
        if isinstance(self.data,np.ndarray):
            n_clusters = optimalK(self.data, cluster_array=np.arange(self.min_clusters, self.max_clusters))
        else:
            numpy_data = self.data.numpy()
            n_clusters = optimalK(numpy_data, cluster_array=np.arange(self.min_clusters, self.max_clusters))
        return n_clusters
        # min_gap_diff = float('inf')
        # prev_gap = 0
        # for k in range(self.min_clusters, self.max_clusters):
        #     refDisps = np.zeros(nrefs)
        #     for i in range(nrefs):
        #         # Create new random reference set
        #         randomReference = np.random.random_sample(size=self.data.shape)
        #         # Fit to it
        #         km = KMeans(k)
        #         km.fit(randomReference)
        #         refDisp = km.inertia_
        #         refDisps[i] = refDisp

        #     km = KMeans(k)
        #     km.fit(self.data)
        #     origDisp = km.inertia_
        #     gap = np.log(np.mean(refDisps)) - np.log(origDisp)
        #     if gap-prev_gap>0 and min_gap_diff>gap-prev_gap:
        #         optimal_k = k-1
        #         min_gap_diff = gap-prev_gap
        # return optimal_k
    
    def elbow_visualizer(self,metric='distortion'):
        visualizer = KElbowVisualizer(self.model,k=(self.min_clusters,self.max_clusters),metric=metric)
        visualizer.fit(self.data)
        return visualizer.elbow_value_
    
    
def calc_clusters(duration,fps):
    """
    Approximates video and text clusters to be a function of the duration of the entire video

    Args:
        duration ([int]): length of the entire video
        fps ([int]): frames per second

    Returns:
        vc_clusters,text_clusters([int,int]): approximates 2.5 of sentences with each key frame
    """
    total_frames = duration*fps
    
    if duration<=300:
        vc_clusters = total_frames//300
    
    elif duration>300 and duration<=900:
        vc_clusters = total_frames//800
        
    elif duration>900 and duration<=1800:
        vc_clusters = total_frames//1000
    
    elif duration>1800 and duration<=2700:
        vc_clusters = total_frames//1300
    
    else:
        vc_clusters = total_frames/2000
        
    text_clusters = int(vc_clusters*2.25)
    return vc_clusters,text_clusters

def dirgetcheck(main,sub):
    """
    Checks if a directory exists in a location and creates a directory if it doesn't exist
    Args:
        main ([string]): Parent directory
        sub ([string]): Sub directory

    Returns:
        dir([path]) : path of the exisiting/created directory
    """
    dir = os.path.join(os.getcwd(),main)
    dir = os.path.join(dir,sub)
    if not os.path.isdir(dir):
        os.makedirs(dir)
    return dir

def getclusters(data,n_clusters,range=8):
    """
    Takes in the baseline and calculates optimal number of clusters.
    Args:
        data ([Array]): Text/Video features
        n_clusters ([int]): Baseline number of clusters
        range (int, optional): range of values for KMeans training for gapstatistics . Defaults to 5.

    Returns:
        clusters([int]): optimal number of clusters
    """
    if n_clusters>range:
        min_clusters = n_clusters-range
    else:
        min_clusters = 1
    max_clusters = n_clusters+range
    obj = OptimalClusters(data,min_clusters,max_clusters)
    clusters = obj.gap_statistic()
    return clusters
        