from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file
from report_generator import generate_report


# Plagiarism imports
from plagiarism.plagiarism_service import analyze_plagiarism
from plagiarism.feedback import generate_plagiarism_feedback

# AI detection imports
from ai_detection.ai_detector import detect_ai_text
from ai_detection.ai_feedback import generate_ai_feedback

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"].strip()

    if not text:
        return jsonify({"error": "Empty text"}), 400

    # ---------- PLAGIARISM ANALYSIS ----------
    plagiarism_score, plagiarism_details = analyze_plagiarism(text)
    plagiarism_feedback = generate_plagiarism_feedback(
        plagiarism_score, plagiarism_details
    )

    # ---------- AI DETECTION ----------
    ai_result = detect_ai_text(text)
    ai_feedback = generate_ai_feedback(ai_result["ai_score"])

    # ---------- FINAL RESPONSE ----------
    return jsonify({
        "plagiarism_score": plagiarism_score,
        "plagiarism_details": plagiarism_details,
        "feedback": plagiarism_feedback,
        "ai_result": {
            "score": ai_result["ai_score"],
            "label": ai_result["label"],
            "feedback": ai_feedback,
            "sentences": ai_result["ai_sentences"]
        }
    })
@app.route("/download-report", methods=["POST"])
def download_report():
    data = request.get_json()
    filepath = generate_report(data)
    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
