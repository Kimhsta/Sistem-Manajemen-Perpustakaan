# database/db.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "library.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # users (opsional: untuk login, bisa diisi nanti)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin','mahasiswa'))
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nim TEXT UNIQUE NOT NULL,
        nama TEXT NOT NULL,
        prodi TEXT,
        angkatan INTEGER,
        status TEXT DEFAULT 'aktif'
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kode TEXT UNIQUE NOT NULL,
        judul TEXT NOT NULL,
        penulis TEXT,
        penerbit TEXT,
        tahun INTEGER,
        stok_total INTEGER NOT NULL DEFAULT 0,
        stok_tersedia INTEGER NOT NULL DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS loans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        qty INTEGER NOT NULL DEFAULT 1,
        loan_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        return_date TEXT,
        total_fine INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE RESTRICT,
        FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE RESTRICT
    )
    """)

    conn.commit()
    conn.close()
