import nltk
import string

def extract_keywords(desc : str):
    # Extracts keywords from the passed course description
    # @param desc: the course description
    # @returns a list of keywords
    remove_punct = str.maketrans('', '', string.punctuation)
    words = desc.split()
    words = [w.translate(remove_punct) for w in words]
    words = [word.lower() for word in words]
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    return words