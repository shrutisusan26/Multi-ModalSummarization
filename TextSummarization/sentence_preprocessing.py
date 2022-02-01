from sklearn.feature_extraction.text import TfidfVectorizer
import torch
import nltk
from nltk.stem import WordNetLemmatizer 
nltk.download('stopwords')
nltk.download('wordnet')
import gensim
import re

def check_sentence_length(sentence):
    """
    Returns sentences with length greater than 3
    Args:
        sentence ([list]): List of words corresponding to a sentence
    Returns:
        Boolean: True if a sentence is > 3 
    """
    return True if len(sentence)>3 else False

def compute_tfidf(sentences):
    """
    Fits TF-IDF to sentences 
    Args:
        sentences ([type]): All sentences
    Returns:
        tdidf[Array], features[Dict]: Document-term matrix, mapping of terms and  indices 
    """
    tfidf_vectorizer = TfidfVectorizer()
    tfidf = tfidf_vectorizer.fit_transform(sentences)
    tfidf = tfidf.toarray()
    features = tfidf_vectorizer.vocabulary_
    return tfidf, features

def compute_word_weights(sentence,token_embeddings,tfidf,features,sentence_no):
    """
    Computes tf-idf weights with respect to each word in a sentence
    Args:
        sentence ([string]): Current sentence 
        token_embeddings ([tensor]): Embeddings  for tokens formed from the last 4 layers of bert
        tfidf ([Array]):  Document-term matrix
        features ([Dict]): Mapping of terms and indices
        sentence_no ([int]): Index of the current sentences

    Returns:
        embedding,tf_wts[tensor,int]: Sum of BERT embeddings for all words,sum of tfidf values from document-term matrix
    """
    embedding = torch.zeros([1,3072])
    tf_wts = 0
    for j in range(len(sentence.split())):
        w = sentence.split()[j]
        embedding = torch.add(embedding,tfidf[sentence_no][features[w]]*token_embeddings[j])
        tf_wts += tfidf[sentence_no][features[w]]
    return embedding, tf_wts

def lemmatize(text):
    """
    Applies WordNet lemmatization for each word
    Args:
        text ([string]): Word to be lemmatized

    Returns:
        [strng]: Lemmatized word
    """
    return WordNetLemmatizer().lemmatize(text, pos='v')

def preprocess(sentences):

    """
    Returns preprocessed sentences after applying lemmatization,
    removal of stopwords, newlines and sentences with less than 3 words
    
    Returns:
        [list]: preprocessed sentences
    """
    sentences = [re.sub("\\n","",i) for i in sentences]
    letters_only_text = [re.sub("[^a-zA-Z]", " ", i) for i in sentences]
    sentence_words = [i.lower() for i in letters_only_text]

    return [" ".join([lemmatize(token) for token in gensim.utils.simple_preprocess(i) if (token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3) ]) for i in sentence_words]