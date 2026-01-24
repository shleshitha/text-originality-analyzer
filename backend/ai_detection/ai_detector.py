from .features import extract_features

def detect_ai_text(text):
    features = extract_features(text)

    if not features or not features.get("sentence_lengths"):
        return {
            "ai_likelihood": 0,
            "patterns": [],
            "sentences": [],
            "summary": "Text too short for reliable stylistic analysis."
        }

    score = 0.0
    patterns = []

    avg_len = features.get("avg_sentence_len", 0)
    var = features.get("normalized_variance", 1)
    lex = features.get("lexical_diversity", 1)
    bigram_rep = features.get("bigram_repetition", 0)
    func_ratio = features.get("function_word_ratio", 0)
    comma = features.get("comma_density", 0)
    sent_lens = features.get("sentence_lengths", [])

    # Pattern detection + scoring
    if avg_len > 18 and var < 0.6:
        score += 0.25
        patterns.append("Uniform sentence structure")

    if lex < 0.45:
        score += 0.15
        patterns.append("Low lexical diversity")

    if bigram_rep > 0.02:
        score += 0.25
        patterns.append("Repeated phrase patterns")

    if func_ratio > 0.08:
        score += 0.15
        patterns.append("High use of connective words")

    if comma > 1.4:
        score += 0.10
        patterns.append("Consistent punctuation patterns")

    if sent_lens and (max(sent_lens) - min(sent_lens)) < 10:
        score += 0.10
        patterns.append("Low sentence-length variability")

    score = min(score, 1.0)
    likelihood = round(score * 100, 2)

    # Sentence-level evidence
    flagged_sentences = []

    sentences = [s.strip() for s in text.split(".") if len(s.split()) > 8]

    for s in sentences:
        words = s.split()

        # Rule 1: Long & uniform sentences
        if avg_len > 18 and len(words) > avg_len:
            flagged_sentences.append(s)
            continue

        # Rule 2: Heavy use of connectors
        connector_count = sum(
            1 for w in words
            if w.lower() in {
                "and","or","but","however","therefore","thus",
                "moreover","although","because"
            }
        )
        if connector_count >= 2:
            flagged_sentences.append(s)
            continue

        # Rule 3: Comma-heavy structured sentence
        if s.count(",") >= 2:
            flagged_sentences.append(s)
            continue

    # Limit examples for UI clarity
    flagged_sentences = flagged_sentences[:5]


    return {
        "ai_likelihood": likelihood,
        "patterns": patterns,
        "sentences": flagged_sentences,
        "summary": "AI-style likelihood based on linguistic pattern analysis."
    }
