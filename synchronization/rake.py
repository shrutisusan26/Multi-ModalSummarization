import rake 
import operator
import gensim
import re

def preprocess(raw_text):

    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)

    # convert to lower case and split 
    words = letters_only_text.lower()

    return " ".join([token for token in gensim.utils.simple_preprocess(words) if (token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3) ])

def rake(text):
    preprocessed_text = preprocess(text)
    r = rake()
    r.extract_keywords_from_text(preprocessed_text)
    return r.get_ranked_phrases_with_scores()


    