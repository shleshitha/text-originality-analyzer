import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
import nltk
import os

nltk.download("punkt")
from nltk.tokenize import sent_tokenize


# =====================================================
# CONFIG
# =====================================================
SERPAPI_KEY = "cda1961bfe90faba4c7437324da0c80e41ebb92768fef78577e9fe07c82627ea"

TRUSTED_DOMAINS = (
   "wikipedia.org",
    "britannica.com",
    "freecodecamp.org",
    "howstuffworks.com",
    "docs.python.org"
)


# =====================================================
# HELPERS
# =====================================================
def is_trusted_source(url):
    return any(domain in url for domain in TRUSTED_DOMAINS)


def char_similarity(a, b):
    """Character-level similarity for exact copy boost"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def chunk_text(text, size=300):
    """Split long text into smaller chunks (avoid dilution)"""
    words = text.split()
    return [
        " ".join(words[i:i + size])
        for i in range(0, len(words), size)
    ]


def fetch_page_text(url):
    """Fetch clean textual content from a webpage"""
    try:
        r = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        paragraphs = soup.find_all("p")
        return " ".join(p.get_text(strip=True) for p in paragraphs)

    except Exception:
        return ""


def serpapi_search(query):
    """Google search via SerpAPI"""
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 5
    }

    r = requests.get(
        "https://serpapi.com/search",
        params=params,
        timeout=10
    )

    data = r.json()
    urls = []

    for item in data.get("organic_results", []):
        link = item.get("link")
        if link and is_trusted_source(link):
            urls.append(link)

    return list(set(urls))


def build_queries(sentence):
    """
    Build a domain-restricted Google query so that
    SerpAPI searches ONLY selected popular article domains
    """
    words = sentence.split()
    base = " ".join(words[:10])

    domain_filter = " OR ".join(
        [f"site:{domain}" for domain in TRUSTED_DOMAINS]
    )

    # Primary exact phrase search
    query = f'({domain_filter}) "{base}"'

    # Fallback without quotes (still restricted)
    fallback = f'({domain_filter}) {base}'

    return [query, fallback]


# =====================================================
# MAIN PLAGIARISM FUNCTION
def analyze_plagiarism(text):
    sentences = [
        s for s in sent_tokenize(text)
        if len(s.split()) > 8
    ]

    matches = []

    for sentence in sentences[:5]:  # limit for performance
        urls = []

        for query in build_queries(sentence):
            urls.extend(serpapi_search(query))

        urls = list(set(urls))  # deduplicate URLs

        for url in urls:
            page_text = fetch_page_text(url)
            if not page_text:
                continue

            for chunk in chunk_text(page_text):
                vectorizer = TfidfVectorizer(stop_words="english")
                vectors = vectorizer.fit_transform([sentence, chunk])

                tfidf_sim = cosine_similarity(
                    vectors[0:1], vectors[1:2]
                )[0][0]

                char_sim = char_similarity(sentence, chunk)

                # Low threshold, as decided
                if tfidf_sim >= 0.35 or char_sim >= 0.45:
                    matches.append({
                        "sentence": sentence,
                        "source": url
                    })
                    break  # stop chunk loop, go to next URL

    # Decide at the END
    is_plagiarised = len(matches) > 0

    # OPTIONAL: limit to top 5 matches for UI cleanliness
    matches = matches[:5]

    return {
        "is_plagiarised": is_plagiarised,
        "matches": matches
    }

