function scrollToInput() {
  document.getElementById("inputSection")
    .scrollIntoView({ behavior: "smooth" });
}

/* ---------- FILE UPLOAD ---------- */
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
  };
  reader.readAsText(file);
});

/* ---------- ANALYZE ---------- */
function analyze() {
  const text = document.getElementById("textInput").value.trim();

  if (!text) {
    alert("Please enter or upload some text.");
    return;
  }

  fetch("http://127.0.0.1:5000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  })
  .then(res => res.json())
  .then(data => {

    const resultSection = document.getElementById("resultSection");
    const feedbackContent = document.getElementById("feedbackContent");
    const toggleBtn = document.querySelector(".toggle-btn");

    /* FORCE VISIBILITY */
    resultSection.style.display = "block";
    feedbackContent.style.display = "block";
    toggleBtn.innerHTML = "Hide Feedback ▲";

    resultSection.scrollIntoView({ behavior: "smooth" });

    /* ---------- SCORES ---------- */
    document.getElementById("scoreBox").innerHTML = `
      <div class="score-card">
        📄 <b>Plagiarism Score:</b> ${data.plagiarism_score}%
      </div>
      <div class="score-card">
        🤖 <b>AI Generated Score:</b> ${data.ai_result.score}%
        <br><i>${data.ai_result.label}</i>
      </div>
    `;

    /* ---------- FEEDBACK ---------- */
    document.getElementById("feedbackList").innerHTML = `
      <li>${data.feedback}</li>
      <li><b>AI Insight:</b> ${data.ai_result.feedback}</li>
    `;

    /* ---------- PLAGIARISED CONTENT ---------- */
    const plagSection = document.getElementById("plagSection");
    plagSection.style.display = "none";
    plagSection.innerHTML = "";

    if (data.plagiarism_details.length > 0) {
      data.plagiarism_details.forEach(item => {
        plagSection.innerHTML += `
          <div class="highlight-item-red">
            <b>${item.similarity}% similarity</b><br>
            ${item.sentence}
          </div>
        `;
      });
    } else {
      plagSection.innerHTML =
        `<div class="none-text">No plagiarised content detected.</div>`;
    }

    /* ---------- AI GENERATED CONTENT ---------- */
    const aiSection = document.getElementById("aiSection");
    aiSection.style.display = "none";
    aiSection.innerHTML = "";

    if (data.ai_result.sentences.length > 0) {
      data.ai_result.sentences.forEach(sentence => {
        aiSection.innerHTML += `
          <div class="highlight-item-blue">
            ${sentence}
          </div>
        `;
      });
    } else {
      aiSection.innerHTML =
        `<div class="none-text">No AI-generated content detected.</div>`;
    }
  })
  .catch(err => {
    console.error(err);
    alert("Backend error. Check console.");
  });
}

/* ---------- TOGGLE FEEDBACK ---------- */
function toggleFeedback() {
  const feedback = document.getElementById("feedbackContent");
  const btn = document.querySelector(".toggle-btn");

  if (feedback.style.display === "none") {
    feedback.style.display = "block";
    btn.innerHTML = "Hide Feedback ▲";
  } else {
    feedback.style.display = "none";
    btn.innerHTML = "Show Feedback ▼";
  }
}

/* ---------- TOGGLE ACCORDION SECTIONS ---------- */
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

/* ---------- CLEAR INPUT (FIXED) ---------- */
function clearInput() {
  document.getElementById("textInput").value = "";
  document.getElementById("fileInput").value = "";

  // Hide result & feedback
  document.getElementById("resultSection").style.display = "none";
  document.getElementById("feedbackContent").style.display = "none";

  // Clear highlights
  document.getElementById("plagSection").innerHTML = "";
  document.getElementById("aiSection").innerHTML = "";
}
