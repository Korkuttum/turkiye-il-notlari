"""Türkiye il haritası üzerinden kitap notu tutma uygulaması."""

import os
import sqlite3
from datetime import datetime

from flask import Flask, g, jsonify, render_template, request, send_from_directory

DB_PATH = os.environ.get("DB_PATH", "/data/notlar.db")

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    directory = os.path.dirname(DB_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                province      TEXT NOT NULL,
                province_code INTEGER,
                book          TEXT NOT NULL DEFAULT '',
                text          TEXT NOT NULL DEFAULT '',
                timestamp     TEXT NOT NULL
            )
            """
        )
        # Eski kurulumlar için: book sütunu yoksa ekle.
        sutunlar = {r[1] for r in conn.execute("PRAGMA table_info(notes)")}
        if "book" not in sutunlar:
            conn.execute("ALTER TABLE notes ADD COLUMN book TEXT NOT NULL DEFAULT ''")
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_notes_province ON notes(province, timestamp)"
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_notes_book ON notes(book)")
    conn.close()


def row_to_note(row):
    return {
        "id": row["id"],
        "province": row["province"],
        "province_code": row["province_code"],
        "book": row["book"],
        "text": row["text"],
        "timestamp": row["timestamp"],
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/summary")
def summary():
    """Her il için not sayısı — haritayı renklendirmek ve rozet basmak için."""
    rows = get_db().execute(
        "SELECT province, COUNT(*) AS adet FROM notes GROUP BY province"
    ).fetchall()
    return jsonify({row["province"]: row["adet"] for row in rows})


@app.route("/api/notes")
def list_notes():
    province = (request.args.get("province") or "").strip()
    if not province:
        return jsonify({"province": "", "notes": []})

    rows = get_db().execute(
        "SELECT * FROM notes WHERE province = ? ORDER BY timestamp DESC, id DESC",
        (province,),
    ).fetchall()
    return jsonify({"province": province, "notes": [row_to_note(r) for r in rows]})


@app.route("/api/notes", methods=["POST"])
def add_note():
    data = request.get_json(silent=True) or {}
    province = (data.get("province") or "").strip()
    book = (data.get("book") or "").strip()
    text = (data.get("text") or "").strip()
    code = data.get("province_code")

    if not province:
        return jsonify({"error": "İl seçilmedi."}), 400
    if not book:
        return jsonify({"error": "Kitap adı zorunludur."}), 400

    try:
        code = int(code) if code is not None else None
    except (TypeError, ValueError):
        code = None

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    with db:
        cur = db.execute(
            """
            INSERT INTO notes (province, province_code, book, text, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (province, code, book, text, timestamp),
        )
    row = db.execute("SELECT * FROM notes WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(row_to_note(row)), 201


@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    db = get_db()
    with db:
        cur = db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    return jsonify({"deleted": cur.rowcount})


@app.route("/api/books")
def list_books():
    """Daha önce girilmiş kitap adları — formda otomatik tamamlama için."""
    rows = get_db().execute(
        "SELECT DISTINCT book FROM notes WHERE book <> '' ORDER BY book COLLATE NOCASE"
    ).fetchall()
    return jsonify([r["book"] for r in rows])


@app.route("/sw.js")
def service_worker():
    """Service worker kök kapsamdan sunulmalı."""
    return send_from_directory(app.static_folder, "sw.js", mimetype="application/javascript")


@app.route("/api/export")
def export_notes():
    """Tüm notlar — yedekleme / dışa aktarma için."""
    rows = get_db().execute(
        "SELECT * FROM notes ORDER BY province COLLATE NOCASE, timestamp"
    ).fetchall()
    return jsonify([row_to_note(r) for r in rows])


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
