import random
from rmrbot.database.db import get_connection
from datetime import datetime


def get_quote_for_posting():
    """
    Returns one quote eligible for posting.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, text
            FROM quotes
            WHERE is_running_relevant = true
            AND (
                last_posted IS NULL
                OR last_posted < NOW() - INTERVAL '28 days'
            )
            ORDER BY RANDOM()
            LIMIT 1
        """)

        row = cur.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "text": row[1]
        }

    finally:
        cur.close()
        conn.close()

def insert_quote(text, score, is_relevant, conn=None):
    own_conn = False

    if conn is None:
        conn = get_connection()
        own_conn = True

    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO quotes (text, similarity_score, is_running_relevant)
            VALUES (%s, %s, %s)
            """,
            (text, score, is_relevant),
        )

        if own_conn:
            conn.commit()

        return True, None

    except Exception as e:
        return False, str(e)

    finally:
        cur.close()
        if own_conn:
            conn.close()


def get_all_quotes():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, text FROM quotes")
        rows = cur.fetchall()
        return [{"id": r[0], "text": r[1]} for r in rows]
    finally:
        conn.close()


def mark_as_posted(quote_id):

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE quotes
            SET last_posted = NOW()
            WHERE id = %s
        """, (quote_id,))

        conn.commit()

    finally:
        cur.close()
        conn.close()


def update_similarity(quote_id, score, is_relevant):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE quotes
            SET similarity_score = %s,
                is_running_relevant = %s
            WHERE id = %s
        """, (score, is_relevant, quote_id))
        conn.commit()
    finally:
        cur.close()
        conn.close()
