import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download("punkt")

def detect_ai_text(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    if not sentences or not words:
        return {
            "ai_score": 0,
            "label": "Unknown",
            "ai_sentences": []
        }

    avg_sentence_len = sum(len(word_tokenize(s)) for s in sentences) / len(sentences)
    avg_word_len = sum(len(w) for w in words) / len(words)

    sentence_lengths = [len(word_tokenize(s)) for s in sentences]
    sentence_variance = max(sentence_lengths) - min(sentence_lengths)

    ai_probability = 0.0

    # Heuristic rules
    if avg_sentence_len > 18:
        ai_probability += 0.3

    if avg_word_len > 5:
        ai_probability += 0.2

    if sentence_variance < 6:
        ai_probability += 0.3

    if text.count(",") > 6:
        ai_probability += 0.2

    ai_probability = min(ai_probability, 1.0)

    # Sentence-level AI suspicion
    ai_sentences = []
    for s in sentences:
        if len(word_tokenize(s)) > 20:
            ai_sentences.append(s)

    label = (
        "Likely AI-Generated" if ai_probability >= 0.7
        else "Mixed Writing Style" if ai_probability >= 0.4
        else "Human-Written"
    )

    return {
        "ai_score": int(ai_probability * 100),
        "label": label,
        "ai_sentences": ai_sentences
    }
