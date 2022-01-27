from os import truncate
import torch
from transformers import BertTokenizer
import numpy as np
#import matplotlib.pyplot as plt

import nltk
from nltk.stem import WordNetLemmatizer 
nltk.download('stopwords')
nltk.download('wordnet')
import gensim
import re
from TextSummarization.sentence_preprocessing import check_sentence_length, compute_tfidf, compute_word_weights

def lemmatize(text):
    return WordNetLemmatizer().lemmatize(text, pos='v')

def preprocess(sentences):

    # keep only words
    letters_only_text = [re.sub("[^a-zA-Z]", " ", i) for i in sentences]

    # convert to lower case and split 
    sentence_words = [i.lower() for i in letters_only_text]

    return list(filter(check_sentence_length,[" ".join([lemmatize(token) for token in gensim.utils.simple_preprocess(i) if (token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3) ]) for i in sentence_words]))

def get_encodings_attention(sentences):
    global tfidf
    global features
    sentences = preprocess(sentences)
    tfidf, features = compute_tfidf(sentences)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    encoding= lambda sentences:tokenizer.encode(sentences,add_special_tokens=True,truncation=True)
    sent_enc=[]
    for sent in sentences:
        sent_enc.append(encoding(sent))
    max_len = 0
    for i in sent_enc:
        if len(i) > max_len:
            max_len = len(i)
    padded = np.array([i + [0]*(max_len-len(i)) for i in sent_enc])
    attention_mask = np.where(padded != 0, 1, 0)
    return padded,attention_mask,sentences

def generate_sentence_embeddings(model,sentence):
    padded,attention_mask,sentence = get_encodings_attention(sentence)
    input_ids = torch.tensor(padded)  
    attention_mask = torch.tensor(attention_mask)
    with torch.no_grad():
        outputs= model(input_ids, attention_mask)
    hidden_states = outputs[2]
    token_embeddings = torch.stack(hidden_states, dim=0)
    token_embeddings = token_embeddings.permute(1,2,0,3)
    sent_vec=torch.zeros([0,3072])
    sentence_scoring = {}
    for i, sent in enumerate(token_embeddings):
        token_vecs_cat = torch.zeros([0,3072])
        for token in sent:
            cat_vec = torch.cat((token[-1], token[-2], token[-3], token[-4]), dim=0)
            cat_vec = cat_vec[None,:]
            token_vecs_cat = torch.cat((token_vecs_cat, cat_vec), 0)
        print(sentence[i])
        mean_vec, tf_wts = compute_word_weights(sentence[i],token_vecs_cat,tfidf,features,i)
        sentence_scoring[sentence] = tf_wts/len(sentence[i])
        # mean_vec=torch.mean(token_vecs_cat,dim=0)
        # mean_vec = mean_vec[None,:]
        sent_vec = torch.cat((sent_vec, mean_vec), 0)
    print(sentence_scoring)
    return sent_vec