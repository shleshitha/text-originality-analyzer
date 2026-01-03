from database.db_connection import get_connection

def fetch_all_sentences():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sentence FROM sentences")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
