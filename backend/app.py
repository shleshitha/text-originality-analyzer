from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# ----------------- PLAGIARISM -----------------
from plagiarism.plagiarism_service import analyze_plagiarism

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

    # mode can be: "plagiarism" or "ai"
    mode = data.get("mode")

    response = {"mode": mode}

    # ---------- PLAGIARISM CHECK ----------
    if mode == "plagiarism":
        plagiarism_result = analyze_plagiarism(text)
        response["plagiarism"] = plagiarism_result

    # ---------- AI WRITING STYLE CHECK ----------
    elif mode == "ai":
        ai_result = detect_ai_text(text)
        response["ai_result"] = {
            "score": ai_result["score"],
            "label": ai_result["label"],
            "feedback": ai_result["feedback"],
            "sentences": ai_result["sentences"]
        }

    # ---------- INVALID MODE ----------
    else:
        return jsonify({
            "error": "Invalid mode. Use 'plagiarism' or 'ai'."
        }), 400

    return jsonify(response)


@app.route("/download-report", methods=["POST"])
def download_report():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    filepath = generate_report(data)
    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
