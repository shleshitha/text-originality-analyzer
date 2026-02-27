# Intelligent Detection and Feedback System for Plagiarism and AI-Generated Text

## 📌 Project Overview
This project is a web-based application designed to detect plagiarized content and analyze AI-generated writing patterns. It combines Natural Language Processing (NLP), web-based search, and statistical techniques to evaluate text originality.

The system allows users to input or upload text, perform plagiarism detection using online sources, and estimate AI-generated text probability based on linguistic and statistical features. It also provides feedback to improve writing quality.

---
## 🌐 Live Demo

👉 [Click here to open the application](https://your-project-link.com)


## ⚙️ Technologies Used

Programming & Frameworks:
- Python
- Flask

NLP & Machine Learning:
- NLTK
- scikit-learn
- TF-IDF Vectorization
- Cosine Similarity

Web Technologies:
- HTML
- CSS
- JavaScript

External API:
- SerpAPI (Google Search API)

---

## 🔄 Workflow

### Plagiarism Detection Flow:
1. User inputs text or uploads file
2. Text preprocessing (tokenization, normalization)
3. Sentence segmentation
4. Query generation
5. Search using SerpAPI
6. Retrieve matching web pages
7. Extract text from web pages
8. Compute similarity using TF-IDF and cosine similarity
9. Identify plagiarized sentences
10. Display matched sentences with source URLs

### Writing Style Analysis Flow:
1. Text preprocessing
2. Extract linguistic features (sentence structure, grammar patterns)
3. Extract statistical features (word frequency, sentence length)
4. Analyze patterns
5. Generate AI-style probability score
6. Provide feedback with reasoning

---

## 🚀 How to Run the Project

### 1. Clone the Repository
git clone https://github.com/shleshitha/text-originality-analyzer.git
cd text-originality-analyzer/backend


### 2. Install Dependencies
pip install -r requirements.txt


### 3. Run the Application
python app.py


### 4. Open in Browser
Open index.html file in browser



## 🏗️ System Architecture

The system follows a three-layer architecture:

1. Presentation Layer (Frontend)
   - User interface for input, results display, and report download

2. Application Layer (Flask Backend)
   - Handles requests, routing, and control logic
   - Directs flow to appropriate modules

3. Processing Layer
   - Plagiarism Detection Module
   - Writing Style Analysis Module
   - External Service (SerpAPI)

Note:
- No direct connection between plagiarism and writing style modules
- SerpAPI is used only in plagiarism detection

---

## ⚠️ Limitations

- Depends on internet connectivity for plagiarism detection
- Limited detection of paraphrased content (no deep semantic analysis)
- AI detection is probability-based, not 100% accurate
- Limited support for file formats
- System performance may slow for large inputs

### SerpAPI Limitations:
- Limited number of free API requests per month
- Results depend on available indexed web content
- May not return consistent results for all queries
- Requires API key for access

---

## 🔮 Future Enhancements

- Integration of semantic embeddings (BERT, Sentence-BERT)
- Improved paraphrase detection using deep learning
- Support for PDF and DOCX file formats
- Multilingual plagiarism detection
- Advanced AI detection using transformer models
- Cloud deployment for scalability
- Database integration for storing reports and history

---

## 📊 Output

Plagiarism Output:
- Plagiarism detected / not detected
- Highlighted plagiarized sentences
- Source URLs of matched content

Writing Style Output:
- AI-style probability score
- Linguistic pattern analysis
- Feedback suggestions

---

## 📜 License
This project is developed for academic purposes.

---

## 🙏 Acknowledgment
We thank our faculty and institution for their guidance and support.

---
