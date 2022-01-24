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
    num_padding = video_features.shape[0] - (text_features.shape[0]%video_features.shape[0])
    text_features = np.concatenate((text_features,np.zeros((num_padding,3072))),axis=0)
    num_batches = text_features.shape[0]//video_features.shape[0]
    results = []
    for i in range(num_batches):
        my_cca.fit(video_features, text_features[i*video_features.shape[0]:(i+1)*video_features.shape[0]])
        batch_result = my_cca.predict(video_features)
        print(batch_result)
        print(batch_result.shape)
        results.append(batch_result)
    return results

if __name__ == "__main__":
    cca(r'C:\Users\PROJECT\Desktop\videos\Keynesian economics _ Aggregate demand and aggregate supply _ Macroeconomics _ Khan Academy.mp4')
    