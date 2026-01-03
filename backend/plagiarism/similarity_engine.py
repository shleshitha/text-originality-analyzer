from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityEngine:
    def __init__(self, corpus_sentences):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.corpus_vectors = self.vectorizer.fit_transform(corpus_sentences)
        self.corpus_sentences = corpus_sentences

    def compare(self, sentence):
        vector = self.vectorizer.transform([sentence])
        similarities = cosine_similarity(vector, self.corpus_vectors)[0]
        return similarities.max()
