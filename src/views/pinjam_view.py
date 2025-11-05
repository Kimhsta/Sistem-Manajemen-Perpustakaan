# views/pinjam_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.loan_model import LoanModel, LOAN_DAYS

class PinjamView(tk.Frame):
    """
    Form peminjaman 1 buku per transaksi:
    - Admin: isi NIM + Kode Buku + Qty
    - Mahasiswa: NIM otomatis dari session (username)
    Menampilkan tabel pinjaman aktif untuk NIM terkait.
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
        ttk.Label(header, text="Peminjaman Buku", font=("Segoe UI", 16, "bold")).pack(side="left")
        ttk.Button(header, text="Kembali", command=self._go_back).pack(side="right")

        form = ttk.LabelFrame(self, text="Form Peminjaman", padding=12)
        form.grid(row=1, column=0, sticky="ew", padx=12, pady=(0,8))
        for i in range(3):
            form.columnconfigure(i, weight=1)

        ttk.Label(form, text="NIM").grid(row=0, column=0, sticky="w", pady=3)
        self.ent_nim = ttk.Entry(form)
        self.ent_nim.grid(row=0, column=1, sticky="ew", pady=3)

        ttk.Label(form, text="Kode Buku").grid(row=1, column=0, sticky="w", pady=3)
        self.ent_kode = ttk.Entry(form)
        self.ent_kode.grid(row=1, column=1, sticky="ew", pady=3)

        ttk.Label(form, text="Qty").grid(row=2, column=0, sticky="w", pady=3)
        self.ent_qty = ttk.Entry(form)
        self.ent_qty.insert(0, "1")
        self.ent_qty.grid(row=2, column=1, sticky="w", pady=3)

        btn_pinjam = ttk.Button(form, text="Pinjam", command=self._do_borrow)
        btn_pinjam.grid(row=3, column=1, sticky="w", pady=(6,0))

        hint = ttk.Label(
            form,
            text=f"Catatan: Lama pinjam {LOAN_DAYS} hari. Denda dihitung saat pengembalian jika terlambat.",
            foreground="#666"
        )
        hint.grid(row=4, column=0, columnspan=2, sticky="w", pady=(6,0))

        # Tabel pinjaman aktif
        box = ttk.LabelFrame(self, text="Pinjaman Aktif untuk NIM terkait", padding=12)
        box.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0,12))
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

    # ---------- Actions ----------
    def _do_borrow(self):
        nim = self._current_nim()
        kode = self.ent_kode.get().strip()
        qty_raw = self.ent_qty.get().strip() or "1"

        if not nim or not kode:
            messagebox.showwarning("Perhatian", "NIM dan Kode Buku wajib diisi.")
            return
        if not qty_raw.isdigit() or int(qty_raw) <= 0:
            messagebox.showwarning("Perhatian", "Qty harus angka > 0.")
            return

        try:
            loan_id = LoanModel.borrow(nim, kode, int(qty_raw))
            data = LoanModel.get_by_id(loan_id)
            messagebox.showinfo(
                "Sukses",
                f"Transaksi dibuat.\nLoan ID: {loan_id}\nJudul: {data['judul']}\nJatuh tempo: {data['due_date']}"
            )
            self.ent_kode.delete(0, "end")
            self.ent_qty.delete(0, "end"); self.ent_qty.insert(0, "1")
            self._reload_table()
        except Exception as e:
            messagebox.showerror("Gagal", str(e))
