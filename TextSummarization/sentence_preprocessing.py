import math
from tkinter.ttk import tclobjs_to_py
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import torch

def check_sentence_length(sentence):
    return True if len(sentence)>3 else False

def compute_tfidf(sentences):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf = tfidf_vectorizer.fit_transform(sentences)
    tfidf = tfidf.toarray()
    features = tfidf_vectorizer.vocabulary_
    return tfidf, features

def compute_word_weights(sentence,token_embeddings,tfidf,features,sentence_no):
        
    embedding = torch.zeros(3072)
    tf_wts = 0
    for j in range(len(sentence.split())):
        w = sentence.split()[j]
        embedding = torch.add(embedding,tfidf[sentence_no][features[w]]*token_embeddings[j])
        tf_wts += tfidf[sentence_no][features[w]]
    return embedding
    
    