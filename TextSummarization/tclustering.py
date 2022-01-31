import imp
import requests
from multiprocessing import Pool
from TextSummarization.rake_transcript import rake_transcript
import numpy as np
from sklearn.cluster import KMeans
import re
from sklearn.metrics import pairwise_distances_argmin_min
import time
from TextSummarization.baas import generate_sentence_embeddings
from transformers import BertModel
import json
from helper import dirgetcheck
import os
from TextSummarization.text_preprocessing import preprocess
from TextSummarization.sentence_preprocessing import check_sentence_length

import nltk
from nltk.stem import WordNetLemmatizer 
nltk.download('stopwords')
nltk.download('wordnet')
import gensim
import re

from TextSummarization.sentence_preprocessing import check_sentence_length

def req(sentences):
    model = BertModel.from_pretrained('bert-base-uncased',
                                    output_hidden_states = True, # Whether the model returns all hidden-states.
                                    )
    sentence_embedding = generate_sentence_embeddings(model,sentences)
    sentence_embedding = {"sentence_embedding":sentence_embedding}
    return sentence_embedding['sentence_embedding']


def clean(sentences):
    sentences= [re.sub("\\n","",i) for i in sentences.values()]
    return sentences

def gen_summary(sentences,n_clusters,ip):
    dir = dirgetcheck('Data','feat_op')
    opn = ip.split("\\")[-1].split('.')[0]
    opn = opn.replace(r'\.','')
    opn = opn.replace('\\','')
    opn = opn.replace(':','')
    output_file = opn+'tvop.npy'
    output_file = os.path.join(dir,output_file)
    sentences = {key:val for key, val in sentences.items() if check_sentence_length(val)}
    list_sentences = list(sentences.values())
    preprocessed_sentences = preprocess(list_sentences)
    print(len(preprocessed_sentences))
    sentence_embed=req(preprocessed_sentences)
    keyphrases = rake_transcript(list_sentences)
    vectors = np.array(sentence_embed)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    print(vectors.shape)
    kmeans = kmeans.fit(vectors)
    closest = []
    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_,vectors)
    ordering = [closest[idx].item() for idx in range(n_clusters)]
    n_ordering =[]
    for i in ordering:
        n_ordering.append(i)
        if i==0:
            n_ordering.append(i+1)
            n_ordering.append(i+2)
        if i==1:
            n_ordering.append(i-1)
            n_ordering.append(i+1)
            n_ordering.append(i+2)
        if i == len(list_sentences)-1:
            n_ordering.append(i-1)
            n_ordering.append(i-2)
        if i == len(list_sentences)-2:
            n_ordering.append(i-1)
            n_ordering.append(i-2)
            n_ordering.append(i+1)
        if i!=0 and i!=len(list_sentences)-1 and i!=1 and i!=len(list_sentences)-2:
            n_ordering.append(i-1)
            n_ordering.append(i-2)
            n_ordering.append(i+1)
            n_ordering.append(i+2)
    n_ordering=set(n_ordering)
    ordering = sorted(list(n_ordering))
    flag = 0
    for i in ordering:
        for j in keyphrases:
            if j[1] in list_sentences[i] and j[0]>20:
                flag = 1
                break
        if flag==0:
            ordering.remove(i)
        else:
            flag=0
            
    summary_sentences = {j[0]:j[1] for i,j in enumerate(sentences.items()) if i in ordering}
    summary_vectors = [vectors[i] for i in ordering]
    labels = np.zeros(len(sentences))
    labels[np.array(ordering)] = 1
    
    print(labels)
    if not os.path.exists("train_data.npy"):
        with open("train_data.npy", 'wb') as file:
            np.save(file, summary_vectors)
        with open("labels.npy", 'wb') as file:
            np.save(file, labels)
            
    else:
        with open("train_data.npy","rb") as file:
            preloaded_data = np.load(file)
            preloaded_data = np.concatenate((preloaded_data,summary_vectors))
            
        with open("train_data.npy","wb") as file:
            np.save(file, preloaded_data)
            
        with open("labels.npy","rb") as file:
            preloaded_labels = np.load(file)
            preloaded_labels = np.concatenate((preloaded_labels,labels))
        
        with open("labels.npy","wb") as file:
            np.save(file, preloaded_labels)

    print(summary_sentences)
    print('Clustering Finished')
    np.save(output_file,summary_vectors)
    return summary_sentences     

