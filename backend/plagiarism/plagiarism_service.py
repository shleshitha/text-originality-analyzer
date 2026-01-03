import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize

from database.corpus_fetcher import fetch_all_sentences
from plagiarism.similarity_engine import SimilarityEngine

# Load corpus once
corpus_sentences = fetch_all_sentences()
engine = SimilarityEngine(corpus_sentences)

def analyze_plagiarism(text):
    sentences = sent_tokenize(text)
    plagiarized = []
    total_score = 0

    for sentence in sentences:
        score = engine.compare(sentence)
        total_score += score

        if score > 0.7:
            plagiarized.append({
                "sentence": sentence,
                "similarity": round(score * 100, 2)
            })

    plagiarism_score = round((total_score / max(len(sentences), 1)) * 100, 2)

    return plagiarism_score, plagiarized
