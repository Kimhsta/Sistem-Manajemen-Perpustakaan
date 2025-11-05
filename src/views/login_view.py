# views/login_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from database.db import get_conn

# Utility hash
def hash_password(plain: str) -> str:
    return hashlib.sha256(plain.encode("utf-8")).hexdigest()

class LoginView(tk.Frame):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        container = ttk.Frame(self, padding=24)
        container.grid(row=0, column=0, sticky="nsew")
        for i in range(3):
            container.rowconfigure(i, weight=1)
        container.columnconfigure(0, weight=1)

        title = ttk.Label(container, text="Login Sistem Perpustakaan", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, pady=(0, 16))

        form = ttk.Frame(container)
        form.grid(row=1, column=0, sticky="ew")
        for c in range(2):
            form.columnconfigure(c, weight=1)

        ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.ent_user = ttk.Entry(form)
        self.ent_user.grid(row=0, column=1, sticky="ew", pady=(0, 6))

        ttk.Label(form, text="Password").grid(row=1, column=0, sticky="w")
        self.ent_pass = ttk.Entry(form, show="*")
        self.ent_pass.grid(row=1, column=1, sticky="ew")

        self.var_show = tk.BooleanVar(value=False)
        chk = ttk.Checkbutton(form, text="Tampilkan password", variable=self.var_show, command=self._toggle_pass)
        chk.grid(row=2, column=1, sticky="w", pady=(6, 0))

        btn = ttk.Button(container, text="Masuk", command=self._login)
        btn.grid(row=2, column=0, pady=16)

        tips = ttk.Label(
            container,
            text="Catatan: Mahasiswa gunakan NIM sebagai username.",
            foreground="#666"
        )
        tips.grid(row=3, column=0, pady=(4,0))

        self.bind_all("<Return>", lambda e: self._login())

    def _toggle_pass(self):
        self.ent_pass.config(show="" if self.var_show.get() else "*")

    def _login(self):
        username = self.ent_user.get().strip()
        password = self.ent_pass.get()

        if not username or not password:
            messagebox.showwarning("Perhatian", "Username dan password wajib diisi.")
            return

        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cur.fetchone()

        if not user:
            messagebox.showerror("Gagal", "User tidak ditemukan.")
            return

        if user["password_hash"] != hash_password(password):
            messagebox.showerror("Gagal", "Password salah.")
            return

        role = user["role"]
        # Simpan session ringan di app
        self.app.session = {
            "user_id": user["id"],
            "username": user["username"],
            "role": role
        }

        # Routing: admin → AdminView, mahasiswa → MahasiswaView (pakai NIM = username)
        if role == "admin":
            from views.admin_view import AdminView
            self.app.show(AdminView)
        else:
            from views.mahasiswa_view import MahasiswaView
            self.app.show(MahasiswaView, nim=username)
