import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize

from database.db_connection import get_connection
import os

def load_wikipedia_corpus(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as file:
                content = file.read()

            insert_document(
                title=filename.replace(".txt", "").replace("_", " ").title(),
                source="Wikipedia",
                content=content
            )


def insert_document(title, source, content):
    """
    Inserts a reference document into MySQL
    and stores its sentences in the sentences table.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Insert document
    cursor.execute(
        "INSERT INTO documents (title, source, content) VALUES (%s, %s, %s)",
        (title, source, content)
    )
    document_id = cursor.lastrowid

    # Split into sentences
    sentences = sent_tokenize(content)

    for sentence in sentences:
        cleaned = sentence.strip()
        if cleaned:
            cursor.execute(
                "INSERT INTO sentences (document_id, sentence) VALUES (%s, %s)",
                (document_id, cleaned)
            )

    conn.commit()
    cursor.close()
    conn.close()
