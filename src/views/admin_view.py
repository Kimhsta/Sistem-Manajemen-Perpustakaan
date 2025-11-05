# views/admin_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.db import get_conn
# Import di atas agar tidak circular ketika show()
from views.buku_view import BooksView
from views.mhs_view import StudentsView
from views.pinjam_view import PinjamView
from views.kembali_view import KembaliView
from views.laporan_view import LaporanView

class AdminView(tk.Frame):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        self.app = app
        self._build_ui()
        self._load_summary()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        header = ttk.Frame(self, padding=16)
        header.grid(row=0, column=0, sticky="ew")
        ttk.Label(header, text="Dashboard Admin", font=("Segoe UI", 16, "bold")).pack(side="left")
        ttk.Button(header, text="Keluar", command=self._logout).pack(side="right")

        # Ringkasan
        summary = ttk.LabelFrame(self, text="Ringkasan", padding=16)
        summary.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        for i in range(4):
            summary.columnconfigure(i, weight=1)

        self.lbl_total_buku = ttk.Label(summary, text="Total Buku: -")
        self.lbl_total_buku.grid(row=0, column=0, sticky="w")

        self.lbl_stok_tersedia = ttk.Label(summary, text="Stok Tersedia: -")
        self.lbl_stok_tersedia.grid(row=0, column=1, sticky="w")

        self.lbl_pinjam_aktif = ttk.Label(summary, text="Pinjaman Aktif: -")
        self.lbl_pinjam_aktif.grid(row=0, column=2, sticky="w")

        self.lbl_telat = ttk.Label(summary, text="Terlambat: -")
        self.lbl_telat.grid(row=0, column=3, sticky="w")

        # Navigasi
        nav = ttk.LabelFrame(self, text="Navigasi", padding=16)
        nav.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))
        for i in range(3):
            nav.columnconfigure(i, weight=1)

        ttk.Button(nav, text="Kelola Buku (CRUD)",
                    command=lambda: self.app.show(BooksView)).grid(row=0, column=0, sticky="ew", padx=8, pady=4)
        ttk.Button(nav, text="Kelola Mahasiswa (CRUD)",
                    command=lambda: self.app.show(StudentsView)).grid(row=0, column=1, sticky="ew", padx=8, pady=4)
        ttk.Button(nav, text="Peminjaman",
                    command=lambda: self.app.show(PinjamView)).grid(row=1, column=0, sticky="ew", padx=8, pady=4)
        ttk.Button(nav, text="Pengembalian",
                    command=lambda: self.app.show(KembaliView)).grid(row=1, column=1, sticky="ew", padx=8, pady=4)
        ttk.Button(nav, text="Laporan",
                    command=lambda: self.app.show(LaporanView)).grid(row=1, column=2, sticky="ew", padx=8, pady=4)

    def _load_summary(self):
        with get_conn() as conn:
            cur = conn.cursor()
            # total buku & stok tersedia
            cur.execute("SELECT COUNT(*) AS n, SUM(stok_tersedia) AS stok FROM books")
            row = cur.fetchone() or {"n": 0, "stok": 0}
            total_buku = row["n"] or 0
            stok = row["stok"] or 0

            # pinjaman aktif
            cur.execute("SELECT COUNT(*) AS n FROM loans WHERE return_date IS NULL")
            aktif = (cur.fetchone() or {"n": 0})["n"]

            # telat
            cur.execute("""
                SELECT COUNT(*) AS n
                FROM loans
                WHERE return_date IS NULL
                AND DATE(due_date) < DATE('now')
            """)
            telat = (cur.fetchone() or {"n": 0})["n"]

        self.lbl_total_buku.config(text=f"Total Buku: {total_buku}")
        self.lbl_stok_tersedia.config(text=f"Stok Tersedia: {stok}")
        self.lbl_pinjam_aktif.config(text=f"Pinjaman Aktif: {aktif}")
        self.lbl_telat.config(text=f"Terlambat: {telat}")

    def _todo(self):
        messagebox.showinfo("Info", "Laporan akan ditambahkan nanti.")

    def _logout(self):
        self.app.session = {}
        from views.login_view import LoginView
        self.app.show(LoginView)
