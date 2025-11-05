# models/book_model.py
from database.db import get_conn

class BookModel:
    @staticmethod
    def create(kode: str, judul: str, penulis: str = "", penerbit: str = "",
               tahun: int | None = None, stok_total: int = 0):
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO books(kode, judul, penulis, penerbit, tahun, stok_total, stok_tersedia)
                VALUES(?,?,?,?,?, ?, ?)
            """, (kode, judul, penulis, penerbit, tahun, stok_total, stok_total))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def update(book_id: int, **fields):
        if not fields:
            return 0
        cols = ", ".join([f"{k}=?" for k in fields.keys()])
        params = list(fields.values()) + [book_id]
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE books SET {cols} WHERE id=?", params)
            conn.commit()
            return cur.rowcount

    @staticmethod
    def delete(book_id: int):
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM books WHERE id=?", (book_id,))
            conn.commit()
            return cur.rowcount

    @staticmethod
    def get_by_id(book_id: int):
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM books WHERE id=?", (book_id,))
            return cur.fetchone()

    @staticmethod
    def get_by_kode(kode: str):
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM books WHERE kode=?", (kode,))
            return cur.fetchone()

    @staticmethod
    def search(keyword: str = "", limit: int = 50, offset: int = 0):
        kw = f"%{keyword.strip()}%"
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM books
                WHERE kode LIKE ? OR judul LIKE ? OR penulis LIKE ? OR penerbit LIKE ?
                ORDER BY judul ASC LIMIT ? OFFSET ?
            """, (kw, kw, kw, kw, limit, offset))
            return cur.fetchall()

    @staticmethod
    def decrease_stock(book_id: int, qty: int):
        with get_conn() as conn:
            cur = conn.cursor()
            # pastikan stok cukup
            cur.execute("SELECT stok_tersedia FROM books WHERE id=?", (book_id,))
            row = cur.fetchone()
            if not row or row["stok_tersedia"] < qty:
                raise ValueError("Stok tidak cukup.")
            cur.execute("""
                UPDATE books SET stok_tersedia = stok_tersedia - ?
                WHERE id=?
            """, (qty, book_id))
            conn.commit()

    @staticmethod
    def increase_stock(book_id: int, qty: int):
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE books SET stok_tersedia = stok_tersedia + ?
                WHERE id=?
            """, (qty, book_id))
            conn.commit()
