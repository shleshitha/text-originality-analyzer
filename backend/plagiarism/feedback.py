def generate_plagiarism_feedback(score, details):
    if score > 60:
        return "High plagiarism detected. Rewrite highlighted sentences."
    elif score > 30:
        return "Moderate plagiarism. Consider paraphrasing."
    else:
        return "Low plagiarism risk. Good originality."
