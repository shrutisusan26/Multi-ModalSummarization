from TextSummarization.rake_transcript import rake_transcript
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from TextSummarization.baas import generate_sentence_embeddings
from transformers import BertModel
from helper import dirgetcheck
import os
from TextSummarization.sentence_preprocessing import preprocess
from sklearn.decomposition import  TruncatedSVD
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
import re
from helper import getclusters
import scipy

def cosine_distance_between_two_embeddings(v1, v2, th):
    """
    Calculates cosine similarity between 2 vectors.

    Args:
        v1 (np arr): Vector corresponding to a frame.
        v2 (np arr): Vector corresponding to a frame.

    Returns:
        int: Cosine similarty between the 2 vectors.
    """
    cs = 1- scipy.spatial.distance.cosine(v1, v2)
    #print(cs)
    if cs >=th:
        return True
    else:
        return False


def req(sentences):
    """
    Returns:
       sentence_embedding[Dict]: Sentence embeddings from BERT & TFIDF
    """
    model = BertModel.from_pretrained('bert-base-uncased',
                                    output_hidden_states = True, # Whether the model returns all hidden-states.
                                    )
    sentence_embedding = generate_sentence_embeddings(model,sentences)
    sentence_embedding = {"sentence_embedding":sentence_embedding}
    return sentence_embedding['sentence_embedding']

def lsa(kmeans,n_clusters,sentences,all=False,ordering=[]):
    """
    Returns  a score for each sentence after topic modelling with LSA
    Args:
        kmeans ([object]):  kmeans clusters
        n_clusters ([int]): Optimal number of clusters
        sentences ([Dict]): Dictionary  of sentences with timestamp

    Returns:
       summ([string]): Summary sentences 
    """
    if not all:
        summ =[]
        for id in range(n_clusters):
            cluster_sents=[]
            cluster = np.where(kmeans.labels_ == id)[0]
            cluster_sents.extend([list(sentences.values())[m] for m in cluster])
            vectorizer = TfidfVectorizer(stop_words=stop_words,max_features=1000)
            if len(cluster_sents) > 1:
                X = vectorizer.fit_transform(cluster_sents)
                lsa_model = TruncatedSVD(n_components=1, algorithm='randomized', n_iter=10, random_state=42)
                lsa_top=lsa_model.fit_transform(X)
                vocab = vectorizer.get_feature_names()
                k = {}
                for m, comp in enumerate(lsa_model.components_):
                    vocab_comp = zip(vocab, comp)
                    sorted_words = sorted(vocab_comp, key= lambda x:x[1], reverse=True)[:10]
                    for t in sorted_words:
                        k[t[0]] = 1
                sent_score = [0]*len(cluster_sents)

                for i in range(len(cluster_sents)):
                    for j in cluster_sents[i].split():
                        try:
                            sent_score[i]+=k[j]
                        except:
                            continue

                summ.append(cluster[sent_score.index(max(sent_score))])
            else:
                summ.append(cluster[0])
    if all:
        summ = ordering
    sentsumm=[]
    sentsumm.extend([list(sentences.values())[m] for m in summ])
    vectorizer = TfidfVectorizer(stop_words=stop_words,max_features=1000)
    X = vectorizer.fit_transform(sentsumm)
    lsa_model = TruncatedSVD(n_components=1, algorithm='randomized', n_iter=10, random_state=42)
    lsa_top=lsa_model.fit_transform(X)
    vocab = vectorizer.get_feature_names()
    k = {}
    for m, comp in enumerate(lsa_model.components_):
        vocab_comp = zip(vocab, comp)
        sorted_words = sorted(vocab_comp, key= lambda x:x[1], reverse=True)[:10]
        for t in sorted_words:
            k[t[0]] = 1
    sent_score = [0]*len(sentsumm)

    for i in range(len(sentsumm)):
        for j in sentsumm[i].split():
            try:
                sent_score[i]+=k[j]
            except:
                continue
        sent_score[i]=sent_score[i]/len(sentsumm[i].split())
    fsumm = [summ[i] for i in range(len(summ)) if sent_score[i]>0 ]
    #print(len(fsumm))
    #print(sent_score)
    return fsumm

def gen_summary(sentences,ip,n_clusters):
    """
    Generates summary sentences after clustering with KMeans, context sentences
    rake key phrase extraction  & LSA for topic modelling 
    Args:
        sentences (Dict): Dictionary  of sentences with timestamp
        ip (string): Path  to the video file location om server
        n_clusters ([int]): Optimal number of clusters 
    Returns:
        [list]: summary sentences
    """
    dir = dirgetcheck('Data','feat_op')
    opn = ip.split("\\")[-1].split('.')[0]
    opn = re.sub(r'[\.\\:]','',opn)
    output_file = opn+'tvop.npy'
    output_file = os.path.join(dir,output_file)
    list_sentences = list(sentences.values())
    preprocessed_sentences = preprocess(list_sentences)
    sentence_embed=req(preprocessed_sentences)
    n_clusters = getclusters(sentence_embed,n_clusters,3)
    #keyphrases = rake_transcript(list_sentences)
    vectors = np.array(sentence_embed)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans = kmeans.fit(vectors)
    ordering = lsa(kmeans,n_clusters,sentences)
    ordering = sorted(ordering)
    # flag = 0
    # for i in ordering:
    #     for j in keyphrases:
    #         if j[1] in list_sentences[i] and j[0]>20:
    #             flag = 1
    #             break
    #     if flag==0:
    #         ordering.remove(i)
    #     else:
    #         flag=0
    n_ordering =[]
    c_sent = []
    #print(ordering)
    wc_sent = set(ordering)
    for i in ordering:
        n_ordering.append(i)
        if i==0:
            n_ordering += [v for v in [i+1,i+2] if cosine_distance_between_two_embeddings(vectors[i],vectors[v],0.95)]
        if i==1:
            n_ordering += [v for v in [i-1,i+1,i+2] if cosine_distance_between_two_embeddings(vectors[i],vectors[v],0.95)]
        if i == len(list_sentences)-1:
            n_ordering += [v for v in [i-2,i-1] if cosine_distance_between_two_embeddings(vectors[i],vectors[v],0.95)]
        if i == len(list_sentences)-2:
            n_ordering += [v for v in [i-2,i-1,i+1] if cosine_distance_between_two_embeddings(vectors[i],vectors[v],0.95)]
        if i!=0 and i!=len(list_sentences)-1 and i!=1 and i!=len(list_sentences)-2:
            n_ordering += [v for v in [i-2,i-1,i+1,i+2] if cosine_distance_between_two_embeddings(vectors[i],vectors[v],0.95)]
    n_ordering=set(n_ordering)
    c_sent = set(c_sent)
    oc_sent = c_sent-wc_sent
    ordering = sorted(list(n_ordering))
    ordering = lsa(kmeans,n_clusters,sentences,True,ordering)
    ordering = sorted(ordering)
    con_sents = {j[0]:j[1] for i,j in enumerate(sentences.items()) if i in sorted(list(oc_sent))}
    summary_sentences = {j[0]:j[1] for i,j in enumerate(sentences.items()) if i in ordering}
    #print(con_sents)
    summary_vectors = [vectors[i] for i in ordering]
    print('Clustering Finished')
    np.save(output_file,summary_vectors)
    return summary_sentences     

