from .features import extract_features

def detect_ai_text(text):
    features = extract_features(text)

    if not features:
        return {
            "score": 0,
            "label": "Insufficient data",
            "sentences": [],
            "feedback": "Text too short for AI analysis."
        }

    score = 0.0

    if features["avg_sentence_len"] > 22:
        score += 0.20

    if features["sentence_variance"] < 15:
        score += 0.15

    if features["lexical_diversity"] < 0.45:
        score += 0.20

    if features["repetition_ratio"] > 0.08:
        score += 0.15

    if features["function_word_ratio"] > 0.07:
        score += 0.15

    if features["comma_density"] > 1.5:
        score += 0.15

    score = min(score, 1.0)

    percent = round(score * 100, 2)

    if percent >= 70:
        label = "Likely AI-Generated"
    elif percent >= 40:
        label = "Mixed Writing Style"
    else:
        label = "Likely Human-Written"

    ai_sentences = []
    for s in text.split("."):
        if len(s.split()) > 25:
            ai_sentences.append(s.strip())

    return {
        "score": percent,
        "label": label,
        "sentences": ai_sentences,
        "feedback": generate_feedback(percent)
    }

def generate_feedback(score):
    if score >= 70:
        return "Text shows strong indicators of AI-generated writing. Consider rewriting in a more personal tone."
    elif score >= 40:
        return "Text contains a mix of human and AI characteristics."
    else:
        return "Text appears mostly human-written with natural variation."
