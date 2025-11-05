# views/mahasiswa_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.loan_model import LoanModel
from database.db import get_conn
from views.pinjam_view import PinjamView
from views.kembali_view import KembaliView

class MahasiswaView(tk.Frame):
    def __init__(self, app, nim: str, **kwargs):
        super().__init__(app, **kwargs)
        self.app = app
        self.nim = nim
        self._build_ui()
        self._load_profile()
        self._load_active_loans()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        header = ttk.Frame(self, padding=16)
        header.grid(row=0, column=0, sticky="ew")
        self.lbl_title = ttk.Label(header, text=f"Dashboard Mahasiswa", font=("Segoe UI", 16, "bold"))
        self.lbl_title.pack(side="left")
        ttk.Button(header, text="Keluar", command=self._logout).pack(side="right")

        # Info profil
        prof = ttk.LabelFrame(self, text="Profil", padding=16)
        prof.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        for i in range(4):
            prof.columnconfigure(i, weight=1)
        self.lbl_nim = ttk.Label(prof, text="NIM: -")
        self.lbl_nim.grid(row=0, column=0, sticky="w")
        self.lbl_nama = ttk.Label(prof, text="Nama: -")
        self.lbl_nama.grid(row=0, column=1, sticky="w")
        self.lbl_prodi = ttk.Label(prof, text="Prodi: -")
        self.lbl_prodi.grid(row=0, column=2, sticky="w")
        self.lbl_angkatan = ttk.Label(prof, text="Angkatan: -")
        self.lbl_angkatan.grid(row=0, column=3, sticky="w")

        # Navigasi (sementara placeholder)
        nav = ttk.LabelFrame(self, text="Aksi", padding=16)
        nav.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 8))
        nav.columnconfigure(0, weight=1)
        nav.columnconfigure(1, weight=1)
        ttk.Button(nav, text="Pinjam Buku",
                    command=lambda: self.app.show(PinjamView)).grid(row=0, column=0, sticky="ew", padx=8, pady=4)
        ttk.Button(nav, text="Kembalikan Buku",
                    command=lambda: self.app.show(KembaliView)).grid(row=0, column=1, sticky="ew", padx=8, pady=4)
        # Pinjaman aktif
        frame_tbl = ttk.LabelFrame(self, text="Pinjaman Aktif", padding=16)
        frame_tbl.grid(row=3, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.rowconfigure(3, weight=1)
        frame_tbl.rowconfigure(0, weight=1)
        frame_tbl.columnconfigure(0, weight=1)

        cols = ("id", "kode_buku", "judul", "qty", "loan_date", "due_date")
        self.tree = ttk.Treeview(frame_tbl, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=100, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        yscroll = ttk.Scrollbar(frame_tbl, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=0, column=1, sticky="ns")

    def _load_profile(self):
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM students WHERE nim=?", (self.nim,))
            st = cur.fetchone()
        if not st:
            # kalau tidak ketemu, tetap tampilkan NIM agar ketahuan
            self.lbl_nim.config(text=f"NIM: {self.nim}")
            return
        self.lbl_nim.config(text=f"NIM: {st['nim']}")
        self.lbl_nama.config(text=f"Nama: {st['nama']}")
        self.lbl_prodi.config(text=f"Prodi: {st['prodi'] or '-'}")
        self.lbl_angkatan.config(text=f"Angkatan: {st['angkatan'] or '-'}")
        self.lbl_title.config(text=f"Dashboard Mahasiswa – {st['nama']}")

    def _load_active_loans(self):
        self.tree.delete(*self.tree.get_children())
        rows = LoanModel.active_by_nim(self.nim)
        for r in rows:
            self.tree.insert(
                "",
                "end",
                values=(r["id"], r["kode_buku"], r["judul"], r["qty"], r["loan_date"], r["due_date"])
            )

    def _coming(self):
        messagebox.showinfo("Info", "Fitur ini akan dihubungkan ke modul Peminjaman/Pengembalian.")

    def _logout(self):
        self.app.session = {}
        from views.login_view import LoginView
        self.app.show(LoginView)
