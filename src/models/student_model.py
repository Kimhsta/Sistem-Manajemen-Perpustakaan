# models/student_model.py
from database.db import get_conn

class StudentModel:
    @staticmethod
    def create(nim: str, nama: str, prodi: str = "", angkatan: int | None = None, status: str = "aktif"):
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO students(nim, nama, prodi, angkatan, status)
                VALUES(?,?,?,?,?)
            """, (nim, nama, prodi, angkatan, status))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def update(student_id: int, **fields):
        if not fields:
            return 0
        cols = ", ".join([f"{k}=?" for k in fields.keys()])
        params = list(fields.values()) + [student_id]
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE students SET {cols} WHERE id=?", params)
            conn.commit()
            return cur.rowcount

    @staticmethod
    def delete(student_id: int):
        # aman-kan: tidak boleh hapus jika masih ada pinjaman aktif
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT COUNT(*) AS n
                FROM loans
                WHERE student_id=? AND return_date IS NULL
            """, (student_id,))
            if cur.fetchone()["n"] > 0:
                raise ValueError("Mahasiswa masih memiliki pinjaman aktif.")
            cur.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()
            return cur.rowcount

    @staticmethod
    def get_by_id(student_id: int):
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM students WHERE id=?", (student_id,))
            return cur.fetchone()

    @staticmethod
    def get_by_nim(nim: str):
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM students WHERE nim=?", (nim,))
            return cur.fetchone()

    @staticmethod
    def search(keyword: str = "", limit: int = 50, offset: int = 0):
        kw = f"%{keyword.strip()}%"
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM students
                WHERE nim LIKE ? OR nama LIKE ? OR prodi LIKE ?
                ORDER BY nama ASC LIMIT ? OFFSET ?
            """, (kw, kw, kw, limit, offset))
            return cur.fetchall()
