import pandas as pd
import boto
from sklearn.cross_decomposition import CCA

def cca(video_features,text_features):
    my_cca = CCA(n_components=2)
    # Fit the model
    my_cca.fit(video_features, text_features)
    
    return my_cca
    