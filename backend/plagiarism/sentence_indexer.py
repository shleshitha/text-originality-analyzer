import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize

def split_into_sentences(text):
    return [s.strip() for s in sent_tokenize(text) if s.strip()]
