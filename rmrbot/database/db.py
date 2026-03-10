# rmrbot/database/db.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_connection():
    
    required = ["DB_HOST","DB_USER","DB_PASS","DB_NAME","DB_PORT"]
    for k in required:
        if not os.getenv(k):
            raise RuntimeError(f"Missing env var: {k}")

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        dbname=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),
        sslmode="require",
        connect_timeout=5,
    )



def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            text TEXT UNIQUE NOT NULL,
            used BOOLEAN DEFAULT FALSE
        );
        """
    )
    conn.commit()
    conn.close()
