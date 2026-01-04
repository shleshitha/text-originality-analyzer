import re
import math
from collections import Counter

def extract_features(text):
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
    words = re.findall(r'\b\w+\b', text.lower())

    if not sentences or not words:
        return {}

    sentence_lengths = [len(s.split()) for s in sentences]
    avg_sentence_len = sum(sentence_lengths) / len(sentence_lengths)

    variance = sum((l - avg_sentence_len) ** 2 for l in sentence_lengths) / len(sentence_lengths)

    unique_words = len(set(words))
    lexical_diversity = unique_words / len(words)

    repetition_ratio = max(Counter(words).values()) / len(words)

    function_words = {"and","or","but","because","therefore","however","moreover","thus","although"}
    function_word_ratio = sum(1 for w in words if w in function_words) / len(words)

    comma_density = text.count(",") / len(sentences)

    return {
        "avg_sentence_len": avg_sentence_len,
        "sentence_variance": variance,
        "lexical_diversity": lexical_diversity,
        "repetition_ratio": repetition_ratio,
        "function_word_ratio": function_word_ratio,
        "comma_density": comma_density
    }
