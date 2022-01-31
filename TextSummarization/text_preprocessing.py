from TextSummarization.sentence_preprocessing import check_sentence_length
import nltk
from nltk.stem import WordNetLemmatizer 
nltk.download('stopwords')
nltk.download('wordnet')
import gensim
import re

def lemmatize(text):
    return WordNetLemmatizer().lemmatize(text, pos='v')

def preprocess(sentences):

    # keep only words
    letters_only_text = [re.sub("[^a-zA-Z]", " ", i) for i in sentences]
    # convert to lower case and split 
    sentence_words = [i.lower() for i in letters_only_text]
    return [" ".join([lemmatize(token) for token in gensim.utils.simple_preprocess(i) if (token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3) ]) for i in sentence_words]