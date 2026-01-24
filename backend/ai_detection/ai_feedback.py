def generate_feedback(score):
    if score >= 70:
        return "Text shows strong indicators of AI-generated writing. Consider rewriting with more personal variation."
    elif score >= 40:
        return "Text contains a mix of human and AI-like characteristics."
    else:
        return "Text appears mostly human-written with natural variation."
