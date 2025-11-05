from database.db import init_db, get_conn
from models.book_model import BookModel
from models.student_model import StudentModel
from models.loan_model import LoanModel
# main.py
import tkinter as tk

from views.login_view import LoginView

APP_TITLE = "Sistem Informasi Perpustakaan"

def _seed_minimal():
    """Seed 1 admin & 1 mahasiswa & 1 buku (jalankan aman, akan abaikan jika sudah ada)."""
    import hashlib
    def h(p): return hashlib.sha256(p.encode("utf-8")).hexdigest()
    with get_conn() as conn:
        c = conn.cursor()
        # admin
        c.execute("INSERT OR IGNORE INTO users(username, password_hash, role) VALUES(?,?,?)",
                  ("admin", h("admin123"), "admin"))
        # mahasiswa user: username = NIM
        c.execute("INSERT OR IGNORE INTO students(nim, nama, prodi, angkatan, status) VALUES(?,?,?,?,?)",
                  ("230103001", "Budi", "TI", 2023, "aktif"))
        c.execute("INSERT OR IGNORE INTO users(username, password_hash, role) VALUES(?,?,?)",
                  ("230103001", h("budi123"), "mahasiswa"))
        # buku
        c.execute("INSERT OR IGNORE INTO books(kode, judul, penulis, penerbit, tahun, stok_total, stok_tersedia) VALUES(?,?,?,?,?,?,?)",
                  ("BK-001", "Algoritma Dasar", "Tardi S.Kom", "UDB Press", 2024, 5, 5))
        conn.commit()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1000x650")
        self.session = {}
        init_db()
        _seed_minimal()
        self.current = None
        self.show(LoginView)

    def show(self, FrameClass, **kwargs):
        if self.current is not None:
            self.current.destroy()
        self.current = FrameClass(self, **kwargs)
        self.current.pack(fill="both", expand=True)


# 1) siapkan DB & tabel
init_db()

# 2) seed ringkas (jalankan sekali saja)
try:
    mhs_id = StudentModel.create("230103001", "Budi", "TI", 2023, "aktif")
except Exception:
    pass
try:
    bk_id = BookModel.create("BK-001", "Algoritma Dasar", "Tardi S.Kom", "UDB Press", 2024, 5)
except Exception:
    pass

# 3) pinjam buku
loan_id = LoanModel.borrow("230103001", "BK-001", qty=1)
print("Loan ID:", loan_id)

# 4) cek pinjaman aktif
for row in LoanModel.active_by_nim("230103001"):
    print(dict(row))

# 5) kembalikan
denda = LoanModel.return_loan(loan_id)
print("Denda:", denda)

if __name__ == "__main__":
    App().mainloop()
