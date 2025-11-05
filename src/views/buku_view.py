# views/buku_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.book_model import BookModel

class BooksView(tk.Frame):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        self.app = app
        self._build_ui()
        self._load_data()

    # ---------- UI ----------
    def _build_ui(self):
        self.columnconfigure(0, weight=1)

        # Header
        header = ttk.Frame(self, padding=12)
        header.grid(row=0, column=0, sticky="ew")
        ttk.Label(header, text="Kelola Buku", font=("Segoe UI", 16, "bold")).pack(side="left")
        ttk.Button(header, text="Kembali", command=self._go_back).pack(side="right")

        # Toolbar (Search + Buttons)
        toolbar = ttk.Frame(self, padding=(12, 0))
        toolbar.grid(row=1, column=0, sticky="ew")
        toolbar.columnconfigure(1, weight=1)

        ttk.Label(toolbar, text="Cari").grid(row=0, column=0, padx=(0, 6))
        self.ent_search = ttk.Entry(toolbar)
        self.ent_search.grid(row=0, column=1, sticky="ew")
        ttk.Button(toolbar, text="Cari", command=self._search).grid(row=0, column=2, padx=6)
        ttk.Button(toolbar, text="Reset", command=self._reset_search).grid(row=0, column=3)

        btns = ttk.Frame(self, padding=(12, 8))
        btns.grid(row=2, column=0, sticky="ew")
        ttk.Button(btns, text="Tambah", command=self._add_dialog).pack(side="left", padx=(0,6))
        ttk.Button(btns, text="Edit", command=self._edit_dialog).pack(side="left", padx=6)
        ttk.Button(btns, text="Hapus", command=self._delete).pack(side="left", padx=6)
        ttk.Button(btns, text="Refresh", command=self._load_data).pack(side="left", padx=6)

        # Tree
        table = ttk.Frame(self, padding=12)
        table.grid(row=3, column=0, sticky="nsew")
        self.rowconfigure(3, weight=1)

        cols = ("id", "kode", "judul", "penulis", "penerbit", "tahun", "stok_total", "stok_tersedia")
        self.tree = ttk.Treeview(table, columns=cols, show="headings", height=16)
        for c, w in zip(cols, (60, 100, 220, 160, 160, 70, 90, 100)):
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        y = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y.set)
        y.grid(row=0, column=1, sticky="ns")
        table.rowconfigure(0, weight=1)
        table.columnconfigure(0, weight=1)

        # Double-click to edit
        self.tree.bind("<Double-1>", lambda e: self._edit_dialog())

    # ---------- Actions ----------
    def _go_back(self):
        from views.admin_view import AdminView
        self.app.show(AdminView)

    def _load_data(self, keyword: str = ""):
        self.tree.delete(*self.tree.get_children())
        rows = BookModel.search(keyword=keyword, limit=200, offset=0)
        for r in rows:
            self.tree.insert("", "end", values=(
                r["id"], r["kode"], r["judul"], r["penulis"] or "",
                r["penerbit"] or "", r["tahun"] or "",
                r["stok_total"], r["stok_tersedia"]
            ))

    def _search(self):
        self._load_data(self.ent_search.get().strip())

    def _reset_search(self):
        self.ent_search.delete(0, "end")
        self._load_data()

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Info", "Pilih data terlebih dahulu.")
            return None
        vals = self.tree.item(sel[0], "values")
        return int(vals[0])

    def _add_dialog(self):
        BookDialog(self, title="Tambah Buku", on_save=self._create_book)

    def _edit_dialog(self):
        book_id = self._selected_id()
        if not book_id:
            return
        row = BookModel.get_by_id(book_id)
        if not row:
            messagebox.showerror("Error", "Data tidak ditemukan.")
            return
        BookDialog(self, title="Edit Buku", data=row, on_save=lambda data: self._update_book(book_id, data))

    def _create_book(self, data: dict):
        try:
            tahun = int(data["tahun"]) if data["tahun"] else None
            stok_total = int(data["stok_total"])
            BookModel.create(
                kode=data["kode"], judul=data["judul"], penulis=data["penulis"],
                penerbit=data["penerbit"], tahun=tahun, stok_total=stok_total
            )
            messagebox.showinfo("Sukses", "Buku berhasil ditambahkan.")
            self._load_data()
        except Exception as e:
            messagebox.showerror("Gagal", str(e))

    def _update_book(self, book_id: int, data: dict):
        try:
            tahun = int(data["tahun"]) if data["tahun"] else None
            # stok_total update tidak otomatis ubah stok_tersedia di sini (biar aman)
            affected = BookModel.update(
                book_id,
                kode=data["kode"], judul=data["judul"], penulis=data["penulis"],
                penerbit=data["penerbit"], tahun=tahun, stok_total=int(data["stok_total"])
            )
            if affected:
                messagebox.showinfo("Sukses", "Buku berhasil diperbarui.")
            self._load_data()
        except Exception as e:
            messagebox.showerror("Gagal", str(e))

    def _delete(self):
        book_id = self._selected_id()
        if not book_id:
            return
        if not messagebox.askyesno("Konfirmasi", "Yakin hapus buku ini?"):
            return
        try:
            BookModel.delete(book_id)
            messagebox.showinfo("Sukses", "Buku dihapus.")
            self._load_data()
        except Exception as e:
            messagebox.showerror("Gagal", str(e))

# ---------- Dialog ----------
class BookDialog(tk.Toplevel):
    def __init__(self, parent: BooksView, title="Buku", data=None, on_save=None):
        super().__init__(parent)
        self.parent = parent
        self.data = data or {}
        self.on_save = on_save
        self.title(title)
        self.resizable(False, False)
        self.grab_set()
        self._build_form()
        self._fill()

    def _build_form(self):
        frm = ttk.Frame(self, padding=12)
        frm.grid(row=0, column=0)

        self.ent_kode = self._row(frm, 0, "Kode")
        self.ent_judul = self._row(frm, 1, "Judul")
        self.ent_penulis = self._row(frm, 2, "Penulis")
        self.ent_penerbit = self._row(frm, 3, "Penerbit")
        self.ent_tahun = self._row(frm, 4, "Tahun")
        self.ent_stok_total = self._row(frm, 5, "Stok Total")

        btns = ttk.Frame(frm)
        btns.grid(row=6, column=0, columnspan=2, pady=(10,0))
        ttk.Button(btns, text="Simpan", command=self._save).pack(side="left", padx=4)
        ttk.Button(btns, text="Batal", command=self.destroy).pack(side="left", padx=4)

    def _row(self, parent, r, label):
        ttk.Label(parent, text=label).grid(row=r, column=0, sticky="w", pady=3)
        e = ttk.Entry(parent, width=40)
        e.grid(row=r, column=1, sticky="w", pady=3)
        return e

    def _fill(self):
        if not self.data:
            return
        self.ent_kode.insert(0, self.data["kode"])
        self.ent_judul.insert(0, self.data["judul"])
        self.ent_penulis.insert(0, self.data["penulis"] or "")
        self.ent_penerbit.insert(0, self.data["penerbit"] or "")
        if self.data["tahun"]:
            self.ent_tahun.insert(0, str(self.data["tahun"]))
        self.ent_stok_total.insert(0, str(self.data["stok_total"]))

    def _save(self):
        payload = {
            "kode": self.ent_kode.get().strip(),
            "judul": self.ent_judul.get().strip(),
            "penulis": self.ent_penulis.get().strip(),
            "penerbit": self.ent_penerbit.get().strip(),
            "tahun": self.ent_tahun.get().strip(),
            "stok_total": self.ent_stok_total.get().strip() or "0",
        }
        # Validasi sederhana
        if not payload["kode"] or not payload["judul"]:
            messagebox.showwarning("Perhatian", "Kode dan Judul wajib diisi.")
            return
        if not payload["stok_total"].isdigit():
            messagebox.showwarning("Perhatian", "Stok Total harus angka.")
            return
        if payload["tahun"] and not payload["tahun"].isdigit():
            messagebox.showwarning("Perhatian", "Tahun harus angka.")
            return

        if self.on_save:
            self.on_save(payload)
        self.destroy()
