import pandas as pd
import boto
from sklearn.cross_decomposition import CCA
from helper import dirgetcheck
import numpy as np
import os

def cca(ip):
    dir = dirgetcheck('Data','feat_op')
    opn = ip.split("\\")[-1].split('.')[0]
    opn = opn.replace(r'\.','')
    opn = opn.replace('\\','')
    opn = opn.replace(':','')
    output_file1 = opn+'op.npy'
    output_file2 = opn+'tvop.npy'
    video_features = np.load(os.path.join(dir,output_file1))
    text_features = np.load(os.path.join(dir,output_file2))
    my_cca = CCA(n_components=2)
    # Fit the model
    print(video_features.shape)
    print(text_features.shape)
    my_cca.fit(video_features, text_features)
    results = my_cca.predict(video_features)
    print(results)
    print(results.shape)
    return results

if __name__ == "__main__":
    cca(r'C:\Users\PROJECT\Desktop\videos\Keynesian economics _ Aggregate demand and aggregate supply _ Macroeconomics _ Khan Academy.mp4')
    