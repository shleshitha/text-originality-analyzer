from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# ----------------- PLAGIARISM -----------------
from plagiarism.plagiarism_service import analyze_plagiarism
from plagiarism.feedback import generate_plagiarism_feedback

# ----------------- AI DETECTION -----------------
from ai_detection.ai_detector import detect_ai_text

# ----------------- REPORT -----------------
from report_generator import generate_report

app = Flask(__name__)
CORS(app)  # allow frontend access


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
    # ai_result already contains: score, label, feedback, sentences

    # ---------- FINAL RESPONSE ----------
    return jsonify({
        "plagiarism_score": plagiarism_score,
        "plagiarism_details": plagiarism_details,
        "feedback": plagiarism_feedback,
        "ai_result": {
            "score": ai_result["score"],
            "label": ai_result["label"],
            "feedback": ai_result["feedback"],
            "sentences": ai_result["sentences"]
        }
    })


@app.route("/download-report", methods=["POST"])
def download_report():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    filepath = generate_report(data)
    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
