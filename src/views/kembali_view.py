# views/kembali_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.loan_model import LoanModel, DAILY_FINE

class KembaliView(tk.Frame):
    """
    Pengembalian buku:
    - Bisa pilih dari tabel pinjaman aktif (lebih aman)
    - Atau masukkan Loan ID langsung
    Menampilkan denda yang dihitung otomatis oleh LoanModel.
    """
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        self.app = app
        self.role = (app.session or {}).get("role", "admin")
        self.nim_session = (app.session or {}).get("username", "")

        self._build_ui()
        self._prefill_nim()
        self._reload_table()

    # ---------- UI ----------
    def _build_ui(self):
        self.columnconfigure(0, weight=1)

        header = ttk.Frame(self, padding=12)
        header.grid(row=0, column=0, sticky="ew")
        ttk.Label(header, text="Pengembalian Buku", font=("Segoe UI", 16, "bold")).pack(side="left")
        ttk.Button(header, text="Kembali", command=self._go_back).pack(side="right")

        # Filter by NIM
        flt = ttk.LabelFrame(self, text="Filter", padding=12)
        flt.grid(row=1, column=0, sticky="ew", padx=12, pady=(0,8))
        flt.columnconfigure(1, weight=1)

        ttk.Label(flt, text="NIM").grid(row=0, column=0, sticky="w", pady=3)
        self.ent_nim = ttk.Entry(flt)
        self.ent_nim.grid(row=0, column=1, sticky="ew", pady=3)
        ttk.Button(flt, text="Muat Pinjaman Aktif", command=self._reload_table).grid(row=0, column=2, padx=8)

        # Tabel
        box = ttk.LabelFrame(self, text="Pinjaman Aktif", padding=12)
        box.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0,8))
        self.rowconfigure(2, weight=1)
        box.rowconfigure(0, weight=1)
        box.columnconfigure(0, weight=1)

        cols = ("id","kode_buku","judul","qty","loan_date","due_date")
        self.tree = ttk.Treeview(box, columns=cols, show="headings", height=12)
        for c,w in zip(cols,(60,100,220,60,100,100)):
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        y = ttk.Scrollbar(box, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y.set)
        y.grid(row=0, column=1, sticky="ns")

        # Aksi
        act = ttk.LabelFrame(self, text="Aksi Pengembalian", padding=12)
        act.grid(row=3, column=0, sticky="ew", padx=12, pady=(0,12))
        for i in range(4):
            act.columnconfigure(i, weight=1)

        ttk.Label(act, text="Loan ID (opsional)").grid(row=0, column=0, sticky="w", pady=3)
        self.ent_loan = ttk.Entry(act)
        self.ent_loan.grid(row=0, column=1, sticky="ew", pady=3)

        ttk.Button(act, text="Kembalikan (dari Loan ID)", command=self._return_by_id).grid(row=0, column=2, padx=8)
        ttk.Button(act, text="Kembalikan (dari Tabel)", command=self._return_by_selection).grid(row=0, column=3, padx=8)

        hint = ttk.Label(
            act,
            text=f"Denda dihitung otomatis: Rp{DAILY_FINE} per hari terlambat.",
            foreground="#666"
        )
        hint.grid(row=1, column=0, columnspan=4, sticky="w", pady=(6,0))

    # ---------- Helpers ----------
    def _go_back(self):
        if self.role == "admin":
            from views.admin_view import AdminView
            self.app.show(AdminView)
        else:
            from views.mahasiswa_view import MahasiswaView
            self.app.show(MahasiswaView, nim=self.nim_session)

    def _prefill_nim(self):
        if self.role == "mahasiswa" and self.nim_session:
            self.ent_nim.delete(0, "end")
            self.ent_nim.insert(0, self.nim_session)
            self.ent_nim.config(state="disabled")

    def _current_nim(self) -> str:
        return self.nim_session if self.role == "mahasiswa" else self.ent_nim.get().strip()

    def _reload_table(self):
        self.tree.delete(*self.tree.get_children())
        nim = self._current_nim()
        if not nim:
            return
        rows = LoanModel.active_by_nim(nim)
        for r in rows:
            self.tree.insert("", "end", values=(
                r["id"], r["kode_buku"], r["judul"], r["qty"], r["loan_date"], r["due_date"]
            ))

    def _selected_loan_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Info", "Pilih salah satu transaksi pada tabel.")
            return None
        vals = self.tree.item(sel[0], "values")
        return int(vals[0])

    # ---------- Actions ----------
    def _return_by_id(self):
        raw = self.ent_loan.get().strip()
        if not raw or not raw.isdigit():
            messagebox.showwarning("Perhatian", "Masukkan Loan ID yang valid.")
            return
        self._do_return(int(raw))

    def _return_by_selection(self):
        loan_id = self._selected_loan_id()
        if not loan_id:
            return
        self._do_return(loan_id)

    def _do_return(self, loan_id: int):
        try:
            fine = LoanModel.return_loan(loan_id)
            info = LoanModel.get_by_id(loan_id)
            messagebox.showinfo(
                "Selesai",
                f"Pengembalian berhasil.\n"
                f"Loan ID: {loan_id}\n"
                f"Judul: {info['judul']}\n"
                f"Denda: Rp{fine}"
            )
            self.ent_loan.delete(0, "end")
            self._reload_table()
        except Exception as e:
            messagebox.showerror("Gagal", str(e))
