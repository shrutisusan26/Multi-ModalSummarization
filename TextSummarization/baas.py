from os import truncate
import torch
import transformers
from transformers import BertTokenizer
import numpy as np
# OPTIONAL: if you want to have more information on what's happening, activate the logger as follows
import logging
#logging.basicConfig(level=logging.INFO)

import matplotlib.pyplot as plt

# # Load pre-trained model tokenizer (vocabulary)
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# # Load pre-trained model (weights)
# model = BertModel.from_pretrained('bert-base-uncased',
#                                   output_hidden_states = True, # Whether the model returns all hidden-states.
#                                 )
def get_encodings_attention(sentence):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    print(transformers.__version__)
    encoding= lambda sentence:tokenizer.encode(sentence,add_special_tokens=True,truncation=True)
    sent_enc=[]
    for sent in sentence:
        sent_enc.append(encoding(sent))
    max_len = 0
    for i in sent_enc:
        if len(i) > max_len:
            max_len = len(i)
    padded = np.array([i + [0]*(max_len-len(i)) for i in sent_enc])
    attention_mask = np.where(padded != 0, 1, 0)
    return padded,attention_mask

def generate_sentence_embeddings(model,sentence):
    padded,attention_mask = get_encodings_attention(sentence)
    input_ids = torch.tensor(padded)  
    attention_mask = torch.tensor(attention_mask)
    with torch.no_grad():
        outputs= model(input_ids, attention_mask)
    hidden_states = outputs[2]
    token_embeddings = torch.stack(hidden_states, dim=0)
    #token_embeddings = torch.squeeze(token_embeddings, dim=1)
    token_embeddings = token_embeddings.permute(1,2,0,3)
    sent_vec=torch.zeros([0,3072])
    for sent in token_embeddings:
        token_vecs_cat = torch.zeros([0,3072])
        for token in sent:
            cat_vec = torch.cat((token[-1], token[-2], token[-3], token[-4]), dim=0)
            cat_vec = cat_vec[None,:]
            token_vecs_cat = torch.cat((token_vecs_cat, cat_vec), 0)
        mean_vec=torch.mean(token_vecs_cat,dim=0)
        mean_vec = mean_vec[None,:]
        sent_vec = torch.cat((sent_vec, mean_vec), 0)
    return sent_vec