# models/loan_model.py
from datetime import date, timedelta
from database.db import get_conn

DAILY_FINE = 1000          # denda per hari
LOAN_DAYS  = 7             # lama pinjam (hari)
MAX_ACTIVE_LOANS = 3       # batas transaksi aktif per mahasiswa

def _today_str() -> str:
    return date.today().isoformat()

def _calc_fine(due_iso: str, ret_iso: str) -> int:
    due = date.fromisoformat(due_iso)
    ret = date.fromisoformat(ret_iso)
    late = (ret - due).days
    return DAILY_FINE * late if late > 0 else 0

class LoanModel:
    @staticmethod
    def count_active_by_student(student_id: int) -> int:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT COUNT(*) AS n FROM loans
                WHERE student_id=? AND return_date IS NULL
            """, (student_id,))
            return cur.fetchone()["n"]

    @staticmethod
    def borrow(nim: str, kode_buku: str, qty: int = 1) -> int:
        """
        Insert transaksi pinjam (1 buku per baris).
        - Validasi: mahasiswa aktif, stok cukup, batas aktif tidak lewat.
        return loan_id
        """
        if qty <= 0:
            raise ValueError("Qty minimal 1.")

        with get_conn() as conn:
            cur = conn.cursor()

            # mahasiswa
            cur.execute("SELECT * FROM students WHERE nim=?", (nim,))
            st = cur.fetchone()
            if not st:
                raise ValueError("Mahasiswa tidak ditemukan.")
            if st["status"] != "aktif":
                raise ValueError("Mahasiswa non-aktif.")

            # batas aktif
            cur.execute("""
                SELECT COUNT(*) AS n FROM loans
                WHERE student_id=? AND return_date IS NULL
            """, (st["id"],))
            if cur.fetchone()["n"] >= MAX_ACTIVE_LOANS:
                raise ValueError("Melebihi batas pinjaman aktif.")

            # buku
            cur.execute("SELECT * FROM books WHERE kode=?", (kode_buku,))
            bk = cur.fetchone()
            if not bk:
                raise ValueError("Buku tidak ditemukan.")
            if bk["stok_tersedia"] < qty:
                raise ValueError("Stok tidak cukup.")

            # kurangi stok
            cur.execute("""
                UPDATE books SET stok_tersedia = stok_tersedia - ?
                WHERE id=?
            """, (qty, bk["id"]))

            loan_date = _today_str()
            due_date  = (date.today() + timedelta(days=LOAN_DAYS)).isoformat()

            # insert loan
            cur.execute("""
                INSERT INTO loans(student_id, book_id, qty, loan_date, due_date, return_date, total_fine)
                VALUES(?,?,?,?,?, NULL, 0)
            """, (st["id"], bk["id"], qty, loan_date, due_date))
            loan_id = cur.lastrowid

            conn.commit()
            return loan_id

    @staticmethod
    def return_loan(loan_id: int) -> int:
        """Set pengembalian, hitung denda, kembalikan stok. return total_fine."""
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM loans WHERE id=?", (loan_id,))
            ln = cur.fetchone()
            if not ln:
                raise ValueError("Transaksi tidak ditemukan.")
            if ln["return_date"] is not None:
                return ln["total_fine"]  # sudah diproses

            # hitung denda
            ret_date = _today_str()
            fine = _calc_fine(ln["due_date"], ret_date)

            # set return
            cur.execute("""
                UPDATE loans SET return_date=?, total_fine=?
                WHERE id=?
            """, (ret_date, fine, loan_id))

            # balikan stok
            cur.execute("""
                UPDATE books SET stok_tersedia = stok_tersedia + ?
                WHERE id=?
            """, (ln["qty"], ln["book_id"]))

            conn.commit()
            return fine

    @staticmethod
    def get_by_id(loan_id: int):
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT l.*, s.nim, s.nama, b.kode AS kode_buku, b.judul
                FROM loans l
                JOIN students s ON s.id = l.student_id
                JOIN books b    ON b.id = l.book_id
                WHERE l.id=?
            """, (loan_id,))
            return cur.fetchone()

    @staticmethod
    def active_by_nim(nim: str):
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT l.*, b.kode AS kode_buku, b.judul
                FROM loans l
                JOIN students s ON s.id = l.student_id
                JOIN books b    ON b.id = l.book_id
                WHERE s.nim=? AND l.return_date IS NULL
                ORDER BY l.loan_date DESC
            """, (nim,))
            return cur.fetchall()

    @staticmethod
    def list_loans(keyword: str = "", limit: int = 50, offset: int = 0):
        """Cari lewat nim/nama/kode/judul."""
        kw = f"%{keyword.strip()}%"
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT l.*, s.nim, s.nama, b.kode AS kode_buku, b.judul
                FROM loans l
                JOIN students s ON s.id = l.student_id
                JOIN books b    ON b.id = l.book_id
                WHERE s.nim LIKE ? OR s.nama LIKE ? OR b.kode LIKE ? OR b.judul LIKE ?
                ORDER BY l.id DESC LIMIT ? OFFSET ?
            """, (kw, kw, kw, kw, limit, offset))
            return cur.fetchall()
