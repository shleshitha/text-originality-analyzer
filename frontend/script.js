/* =========================
   SCROLL TO INPUT
========================= */
function scrollToInput() {
  document.getElementById("inputSection")
    .scrollIntoView({ behavior: "smooth" });
}

/* =========================
   CHARACTER COUNTER
========================= */
function updateCharCounter() {
  const textarea = document.getElementById("textInput");
  const counter = document.getElementById("charCounter");
  const length = textarea.value.length;

  counter.textContent = `${length} / 3000 characters`;

  if (length >= 3000) {
    counter.classList.add("limit");
  } else {
    counter.classList.remove("limit");
  }
}

/* =========================
   FILE UPLOAD
========================= */
document.getElementById("fileInput").addEventListener("change", function () {
  const file = this.files[0];
  if (!file) return;

  if (file.size > 100 * 1024) {
    alert("File too large! Please upload a file under 100 KB.");
    this.value = "";
    return;
  }

  const reader = new FileReader();
  reader.onload = function () {
    document.getElementById("textInput").value =
      reader.result.slice(0, 3000);
    updateCharCounter();
  };
  reader.readAsText(file);
});

/* =========================
   TEXT INPUT LISTENER
========================= */
document.getElementById("textInput")
  .addEventListener("input", updateCharCounter);

/* =========================
   LOADING INDICATOR
========================= */
function showLoading() {
  document.getElementById("loadingBox").style.display = "block";
}
function hideLoading() {
  document.getElementById("loadingBox").style.display = "none";
}

/* =========================
   BUTTON HANDLERS
========================= */
function runPlagiarismCheck() {
  runAnalysis("plagiarism");
}
function runAIStyleCheck() {
  runAnalysis("ai");
}

/* =========================
   MAIN ANALYSIS
========================= */
function runAnalysis(mode) {
  let text = document.getElementById("textInput").value.trim();

  if (!text) {
    alert("Please enter or upload some text.");
    return;
  }

  if (text.length > 3000) {
    alert("Only the first 3000 characters will be analyzed.");
    text = text.slice(0, 3000);
  }

  showLoading();

  fetch("http://127.0.0.1:5000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, mode })
  })
  .then(res => res.json())
  .then(data => {
    hideLoading();
    addFeedback(data, mode);
  })
  .catch(err => {
    hideLoading();
    console.error(err);
    alert("Backend error. Check console.");
  });
}

/* =========================
   ADD FEEDBACK (TIMELINE)
========================= */
function addFeedback(data, mode) {
  const timeline = document.getElementById("feedbackTimeline");
  const box = document.createElement("div");
  box.className = "feedback-box";

  const detailsId = "details_" + Date.now();

  /* ---------- PLAGIARISM ---------- */
  if (mode === "plagiarism") {

    // ✅ NO PLAGIARISM
    if (!data.plagiarism.is_plagiarised) {
      box.innerHTML = `
        <h3>🟢 Plagiarism Check</h3>
        <p><b>Result:</b> Content appears original.</p>
      `;
    }

    // 🚨 PLAGIARISM FOUND
    else {
      let detailsHTML = "";

      data.plagiarism.matches.forEach(item => {
        detailsHTML += `
          <div class="highlight-item-red">
            <b>Matched sentence:</b><br>
            ${item.sentence}<br>
            <small>Source: ${item.source}</small>
          </div>
        `;
      });

      box.innerHTML = `
        <h3>🔴 Plagiarism Check</h3>
        <p><b>Status:</b> Plagiarism Detected</p>

        <div class="highlight-header" onclick="toggleSection('${detailsId}')">
          🔍 View Detected Content <span>▼</span>
        </div>
        <div class="highlight-body" id="${detailsId}" style="display:none;">
          ${detailsHTML}
        </div>
      `;
    }
  }

  /* ---------- AI WRITING STYLE ---------- */
  if (mode === "ai") {
    let aiDetailsHTML = "";

    if (data.ai_result.sentences.length > 0) {
      data.ai_result.sentences.forEach(sentence => {
        aiDetailsHTML += `
          <div class="highlight-item-blue">
            ${sentence}
          </div>
        `;
      });
    } else {
      aiDetailsHTML = `<div class="none-text">No AI-generated patterns detected.</div>`;
    }

    box.innerHTML = `
      <h3>🤖 Writing Style Check</h3>
      <p><b>Result:</b> ${data.ai_result.label}</p>
      <p>${data.ai_result.feedback}</p>

      <div class="highlight-header" onclick="toggleSection('${detailsId}')">
        🔍 View Detected Patterns <span>▼</span>
      </div>
      <div class="highlight-body" id="${detailsId}" style="display:none;">
        ${aiDetailsHTML}
      </div>
    `;
  }

  timeline.prepend(box);
  document.getElementById("resultSection").style.display = "block";
  box.scrollIntoView({ behavior: "smooth" });
}

/* =========================
   TOGGLE INDIVIDUAL SECTION
========================= */
function toggleSection(sectionId) {
  const section = document.getElementById(sectionId);
  const header = section.previousElementSibling;

  if (section.style.display === "block") {
    section.style.display = "none";
    header.classList.remove("active");
  } else {
    section.style.display = "block";
    header.classList.add("active");
  }
}

/* =========================
   TOGGLE ALL FEEDBACK
========================= */
function toggleAllFeedback() {
  const timeline = document.getElementById("feedbackTimeline");
  const btn = document.querySelector(".toggle-btn");

  if (timeline.style.display === "none") {
    timeline.style.display = "block";
    btn.innerHTML = "Hide Feedback ▲";
  } else {
    timeline.style.display = "none";
    btn.innerHTML = "Show Feedback ▼";
  }
}

/* =========================
   CLEAR INPUT & RESULTS
========================= */
function clearInput() {
  document.getElementById("textInput").value = "";
  document.getElementById("fileInput").value = "";
  document.getElementById("feedbackTimeline").innerHTML = "";
  document.getElementById("resultSection").style.display = "none";
  updateCharCounter();
}

/* =========================
   DOWNLOAD REPORT
========================= */
function downloadReport() {
  const timeline = document.getElementById("feedbackTimeline");

  if (!timeline || timeline.children.length === 0) {
    alert("No analysis available to download.");
    return;
  }

  let report = "INTELLIGENT TEXT ANALYSIS REPORT\n";
  report += "---------------------------------\n\n";

  Array.from(timeline.children).forEach((card, idx) => {
    report += `Analysis ${idx + 1}:\n`;
    report += card.innerText + "\n\n";
  });

  const blob = new Blob([report], { type: "text/plain" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "analysis_report.txt";
  link.click();
}
