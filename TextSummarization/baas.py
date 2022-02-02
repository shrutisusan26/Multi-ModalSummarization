import torch
from transformers import BertTokenizer
import numpy as np
from TextSummarization.sentence_preprocessing import compute_tfidf, compute_word_weights

def get_encodings_attention(sentences):
    """ 
    Computes tfids & generates encodings for sentences with   
    padding  and attention mask along with [CLS] & [SEP] 
    to input to BERT model
    Args:
        sentences ([list]): batch of sentences
    Returns:
        padded,attention_mask,sentences ([Array,Array,list]) : Pads sentences to the same length,
        An array of 1's at locations where a token exists 0 otherwise, orginal sentences
    """
    global tfidf
    global features
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

def generate_sentence_embeddings(model,sentences):
    """ 
    Generates encodings using last 4 layers in BERT and TFIDF weight for all sentences
    Args:
        model ([Model]): Bert Pretrained Model
        sentences ([list]): All sentences

    Returns:
        sent_vec[tensor]: Embedding Vectors for sentences
    """
    padded,attention_mask,sentences = get_encodings_attention(sentences)
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
        mean_vec, tf_wts = compute_word_weights(sentences[i],token_vecs_cat,tfidf,features,i)
        try:
            sentence_scoring[sentences[i]] = tf_wts/len(sentences[i])
        except ZeroDivisionError:
            sentence_scoring[sentences[i]] = 0
        sent_vec = torch.cat((sent_vec, mean_vec), 0)
    return sent_vec