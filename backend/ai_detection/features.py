import re
from collections import Counter

FUNCTION_WORDS = {
    "the","a","an","and","or","but","if","while","with","without",
    "because","although","however","therefore","thus","moreover",
    "to","of","in","on","at","by","for","from"
}

def extract_features(text):
    # Improved sentence detection
    sentences = re.findall(r'[^.!?]+[.!?]', text)
    words = re.findall(r'\b\w+\b', text.lower())

    # Minimum text requirement
    if len(sentences) < 3 or len(words) < 30:
        return {}

    sentence_lengths = [len(s.split()) for s in sentences]
    avg_sentence_len = sum(sentence_lengths) / len(sentence_lengths)

    variance = sum((l - avg_sentence_len) ** 2 for l in sentence_lengths) / len(sentence_lengths)
    normalized_variance = variance / (avg_sentence_len + 1e-6)

    lexical_diversity = len(set(words)) / len(words)

    # Bigram repetition (strong AI indicator)
    bigrams = list(zip(words, words[1:]))
    bigram_counts = Counter(bigrams)
    bigram_repetition = max(bigram_counts.values()) / len(bigrams)

    function_word_ratio = sum(1 for w in words if w in FUNCTION_WORDS) / len(words)

    comma_density = text.count(",") / len(sentences)

    return {
        "avg_sentence_len": avg_sentence_len,
        "normalized_variance": normalized_variance,
        "lexical_diversity": lexical_diversity,
        "bigram_repetition": bigram_repetition,
        "function_word_ratio": function_word_ratio,
        "comma_density": comma_density,
        "sentence_lengths": sentence_lengths
    }
