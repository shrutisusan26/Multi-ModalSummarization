import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer

class OptimalClusters:
    def __init__(self, data, min_clusters, max_clusters):
        self.data = data
        self.min_clusters = min_clusters
        self.max_clusters = max_clusters
        self.model = KMeans()
        
    def gap_statistic(self, nrefs=3):
        max_gap = -float('inf')
        for k in range(self.min_clusters, self.max_clusters):
            refDisps = np.zeros(nrefs)
            for i in range(nrefs):
                
                # Create new random reference set
                randomReference = np.random.random_sample(size=self.data.shape)
                
                # Fit to it
                km = KMeans(k)
                km.fit(randomReference)
                
                refDisp = km.inertia_
                refDisps[i] = refDisp

            km = KMeans(k)
            km.fit(self.data)
            
            origDisp = km.inertia_
            gap = np.log(np.mean(refDisps)) - np.log(origDisp)
            
            if gap>=max_gap:
                optimal_k = k
                max_gap = gap
                
        return optimal_k
    
    def elbow_visualizer(self,metric='distortion'):
        visualizer = KElbowVisualizer(self.model,k=(self.min_clusters,self.max_clusters),metric=metric)
        visualizer.fit(self.data)
        return visualizer.elbow_value_
    
    