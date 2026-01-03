def generate_ai_feedback(ai_score):
    if ai_score >= 70:
        return "Text shows strong indicators of AI generation. Consider rewriting in your own words."
    elif ai_score >= 40:
        return "Text appears to have mixed human and AI-generated patterns."
    else:
        return "Text appears predominantly human-written."
