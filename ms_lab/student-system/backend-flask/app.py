import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/students")
def students():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("DB_NAME", "studentdb"),
            user=os.getenv("DB_USER", "admin"),
            password=os.getenv("DB_PASSWORD", "student123")
        )

        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100)
            )
        """)

        cur.execute("""
            INSERT INTO students (name)
            SELECT 'Arun'
            WHERE NOT EXISTS (
                SELECT 1 FROM students WHERE name = 'Arun'
            )
        """)

        cur.execute("SELECT id, name FROM students")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify([
            {"id": row[0], "name": row[1]} for row in rows
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)