from sklearn.feature_extraction.text import TfidfVectorizer
import torch
import nltk
from nltk.stem import WordNetLemmatizer 
nltk.download('stopwords')
nltk.download('wordnet')
import gensim
import re

def check_sentence_length(sentence):
    return True if len(sentence)>3 else False

def compute_tfidf(sentences):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf = tfidf_vectorizer.fit_transform(sentences)
    tfidf = tfidf.toarray()
    features = tfidf_vectorizer.vocabulary_
    return tfidf, features

def compute_word_weights(sentence,token_embeddings,tfidf,features,sentence_no):
        
    embedding = torch.zeros([1,3072])
    tf_wts = 0
    for j in range(len(sentence.split())):
        w = sentence.split()[j]
        embedding = torch.add(embedding,tfidf[sentence_no][features[w]]*token_embeddings[j])
        tf_wts += tfidf[sentence_no][features[w]]
    return embedding, tf_wts

def lemmatize(text):
    return WordNetLemmatizer().lemmatize(text, pos='v')

def preprocess(sentences):

    # keep only words
    sentences = [re.sub("\\n","",i) for i in sentences]
    letters_only_text = [re.sub("[^a-zA-Z]", " ", i) for i in sentences]

    # convert to lower case and split 
    sentence_words = [i.lower() for i in letters_only_text]

    return [" ".join([lemmatize(token) for token in gensim.utils.simple_preprocess(i) if (token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3) ]) for i in sentence_words]