def ai_feedback(score):
    if score >= 70:
        return [
            "High sentence uniformity detected",
            "Low vocabulary variation",
            "Repeated phrasing patterns"
        ]
    elif score >= 40:
        return [
            "Some structured sentence patterns",
            "Moderate repetition"
        ]
    else:
        return [
            "Natural sentence variation",
            "Good lexical diversity"
        ]
