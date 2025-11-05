# views/mhs_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.student_model import StudentModel

class StudentsView(tk.Frame):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        self.app = app
        self._build_ui()
        self._load_data()

    # ---------- UI ----------
    def _build_ui(self):
        self.columnconfigure(0, weight=1)

        header = ttk.Frame(self, padding=12)
        header.grid(row=0, column=0, sticky="ew")
        ttk.Label(header, text="Kelola Mahasiswa", font=("Segoe UI", 16, "bold")).pack(side="left")
        ttk.Button(header, text="Kembali", command=self._go_back).pack(side="right")

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

        table = ttk.Frame(self, padding=12)
        table.grid(row=3, column=0, sticky="nsew")
        self.rowconfigure(3, weight=1)

        cols = ("id", "nim", "nama", "prodi", "angkatan", "status")
        self.tree = ttk.Treeview(table, columns=cols, show="headings", height=16)
        for c, w in zip(cols, (60, 120, 220, 160, 90, 100)):
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        y = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y.set)
        y.grid(row=0, column=1, sticky="ns")
        table.rowconfigure(0, weight=1)
        table.columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", lambda e: self._edit_dialog())

    # ---------- Actions ----------
    def _go_back(self):
        from views.admin_view import AdminView
        self.app.show(AdminView)

    def _load_data(self, keyword: str = ""):
        self.tree.delete(*self.tree.get_children())
        rows = StudentModel.search(keyword=keyword, limit=200, offset=0)
        for r in rows:
            self.tree.insert("", "end", values=(
                r["id"], r["nim"], r["nama"], r["prodi"] or "", r["angkatan"] or "", r["status"] or ""
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
        StudentDialog(self, title="Tambah Mahasiswa", on_save=self._create_student)

    def _edit_dialog(self):
        sid = self._selected_id()
        if not sid:
            return
        row = StudentModel.get_by_id(sid)
        if not row:
            messagebox.showerror("Error", "Data tidak ditemukan.")
            return
        StudentDialog(self, title="Edit Mahasiswa", data=row, on_save=lambda d: self._update_student(sid, d))

    def _create_student(self, data: dict):
        try:
            angkatan = int(data["angkatan"]) if data["angkatan"] else None
            StudentModel.create(
                nim=data["nim"], nama=data["nama"], prodi=data["prodi"],
                angkatan=angkatan, status=data["status"] or "aktif"
            )
            messagebox.showinfo("Sukses", "Mahasiswa ditambahkan.")
            self._load_data()
        except Exception as e:
            messagebox.showerror("Gagal", str(e))

    def _update_student(self, sid: int, data: dict):
        try:
            angkatan = int(data["angkatan"]) if data["angkatan"] else None
            affected = StudentModel.update(
                sid,
                nim=data["nim"], nama=data["nama"], prodi=data["prodi"],
                angkatan=angkatan, status=data["status"] or "aktif"
            )
            if affected:
                messagebox.showinfo("Sukses", "Mahasiswa diperbarui.")
            self._load_data()
        except Exception as e:
            messagebox.showerror("Gagal", str(e))

    def _delete(self):
        sid = self._selected_id()
        if not sid:
            return
        if not messagebox.askyesno("Konfirmasi", "Yakin hapus mahasiswa ini?"):
            return
        try:
            StudentModel.delete(sid)  # sudah punya guard jika masih ada pinjaman aktif
            messagebox.showinfo("Sukses", "Mahasiswa dihapus.")
            self._load_data()
        except Exception as e:
            messagebox.showerror("Gagal", str(e))

# ---------- Dialog ----------
class StudentDialog(tk.Toplevel):
    def __init__(self, parent: StudentsView, title="Mahasiswa", data=None, on_save=None):
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

        self.ent_nim = self._row(frm, 0, "NIM")
        self.ent_nama = self._row(frm, 1, "Nama")
        self.ent_prodi = self._row(frm, 2, "Prodi")
        self.ent_angkatan = self._row(frm, 3, "Angkatan (tahun)")
        # status dropdown
        ttk.Label(frm, text="Status").grid(row=4, column=0, sticky="w", pady=3)
        self.cmb_status = ttk.Combobox(frm, values=["aktif", "non-aktif"], state="readonly", width=37)
        self.cmb_status.grid(row=4, column=1, sticky="w", pady=3)
        self.cmb_status.current(0)

        btns = ttk.Frame(frm)
        btns.grid(row=5, column=0, columnspan=2, pady=(10,0))
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
        self.ent_nim.insert(0, self.data["nim"])
        self.ent_nama.insert(0, self.data["nama"])
        self.ent_prodi.insert(0, self.data["prodi"] or "")
        if self.data["angkatan"]:
            self.ent_angkatan.insert(0, str(self.data["angkatan"]))
        self.cmb_status.set(self.data["status"] or "aktif")

    def _save(self):
        payload = {
            "nim": self.ent_nim.get().strip(),
            "nama": self.ent_nama.get().strip(),
            "prodi": self.ent_prodi.get().strip(),
            "angkatan": self.ent_angkatan.get().strip(),
            "status": self.cmb_status.get().strip(),
        }
        if not payload["nim"] or not payload["nama"]:
            messagebox.showwarning("Perhatian", "NIM dan Nama wajib diisi.")
            return
        if payload["angkatan"] and not payload["angkatan"].isdigit():
            messagebox.showwarning("Perhatian", "Angkatan harus angka (tahun).")
            return

        if self.on_save:
            self.on_save(payload)
        self.destroy()
