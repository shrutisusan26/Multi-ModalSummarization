from rake_nltk import Rake
def rake_transcript(sentences):
    """
    Extracts keyphrases after applying Rake
    """
    r = Rake()
    r.extract_keywords_from_sentences(sentences)
    return r.get_ranked_phrases_with_scores()


    