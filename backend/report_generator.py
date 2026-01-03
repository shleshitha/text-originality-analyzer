from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_report(data):
    filename = "analysis_report.pdf"
    filepath = os.path.join("reports", filename)

    os.makedirs("reports", exist_ok=True)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Plagiarism & AI Detection Report")

    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y -= 30
    c.drawString(40, y, f"Plagiarism Score: {data['plagiarism_score']}%")
    y -= 15
    c.drawString(40, y, f"AI Generated Score: {data['ai_result']['score']}%")
    y -= 15
    c.drawString(40, y, f"AI Label: {data['ai_result']['label']}")

    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "User Input:")
    y -= 15
    c.setFont("Helvetica", 9)

    for line in data["text"].split("\n"):
        c.drawString(40, y, line[:90])
        y -= 12
        if y < 50:
            c.showPage()
            y = height - 40

    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Plagiarised Sentences:")
    y -= 15
    c.setFont("Helvetica", 9)

    if data["plagiarism_details"]:
        for item in data["plagiarism_details"]:
            c.drawString(40, y, f"- {item['sentence'][:90]}")
            y -= 12
    else:
        c.drawString(40, y, "None")

    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "AI-Generated Sentences:")
    y -= 15
    c.setFont("Helvetica", 9)

    if data["ai_result"]["sentences"]:
        for s in data["ai_result"]["sentences"]:
            c.drawString(40, y, f"- {s[:90]}")
            y -= 12
    else:
        c.drawString(40, y, "None")

    c.save()
    return filepath
