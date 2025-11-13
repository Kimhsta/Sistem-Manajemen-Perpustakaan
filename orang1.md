# Sistem Manajemen Perpustakaan (Python + Tkinter + SQLite)

Proyek ini dibuat sebagai tugas kelompok mata kuliah **Pemrograman Python (GUI & Database)**.
Aplikasi ini berfungsi untuk mengelola data buku, mahasiswa, serta transaksi peminjaman dan pengembalian buku dengan antarmuka berbasis **Tkinter** dan penyimpanan **SQLite**.

---

### 👥 Anggota & Pembagian Tugas

| No  | Nama Anggota / Role           | Tugas Utama                                 | File Fokus                                                              | Keterangan                                                                                                                  |
| --- | ----------------------------- | ------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Backend (Database)**        | Buat dan kelola tabel SQLite                | `database/db.py`, `models/*.py`                                         | Menyediakan fungsi CRUD (tambah, hapus, edit, ambil data) untuk tabel `books`, `students`, dan `loans`.                     |
| 2   | **GUI Login & Menu Utama**    | Halaman login dan dashboard admin/mahasiswa | `views/login_view.py`, `views/admin_view.py`, `views/mahasiswa_view.py` | Mengatur autentikasi pengguna dan navigasi ke tampilan sesuai peran (Admin / Mahasiswa).                                    |
| 3   | **CRUD Buku & Mahasiswa**     | Form tambah, edit, hapus buku dan mahasiswa | `views/buku_view.py`, `views/mhs_view.py`                               | Menampilkan data menggunakan **Treeview Tkinter**, serta menyediakan form interaktif untuk CRUD data.                       |
| 4   | **Peminjaman & Pengembalian** | Fitur pinjam & kembalikan buku              | `views/pinjam_view.py`, `views/kembali_view.py`                         | Mengatur logika peminjaman dan pengembalian buku: otomatis mengurangi / menambah stok serta menghitung denda keterlambatan. |

---

### 🧩 Fitur Utama

1. **Login Multi-Role**

   - Admin → dapat mengelola buku, mahasiswa, serta melihat laporan.
   - Mahasiswa → dapat meminjam dan mengembalikan buku.

2. **Manajemen Buku & Mahasiswa**

   - CRUD data menggunakan tampilan Treeview.
   - Validasi input dasar untuk menghindari duplikasi atau data kosong.

3. **Transaksi Peminjaman & Pengembalian**

   - Sistem menghitung otomatis tanggal pinjam dan jatuh tempo (7 hari).
   - Denda dihitung otomatis jika melewati batas waktu.

4. **Database SQLite**

   - Semua data disimpan lokal pada `src/data/library.db`.
   - Struktur tabel dibuat otomatis saat program dijalankan pertama kali.

---

### 🛠️ Teknologi yang Digunakan

- **Python 3.12**
- **Tkinter** – antarmuka GUI
- **SQLite3** – penyimpanan data lokal
- **PyInstaller** – kompilasi aplikasi ke bentuk `.exe` dan Linux binary
- **OpenPyXL** – ekspor laporan ke Excel (opsional)

---

### 📁 Struktur Direktori Proyek

```
Sistem-Manajemen-Perpustakaan-/
│
├── app.py                      # entry utama program (jalankan dari sini)
├── requirements.txt
├── README.md
│
└── src/
    ├── main.py                 # inisialisasi Tkinter & routing utama
    ├── data/                   # database runtime
    │   └── library.db
    ├── database/
    │   └── db.py               # koneksi SQLite + init tabel
    ├── models/
    │   ├── book_model.py
    │   ├── student_model.py
    │   └── loan_model.py
    ├── views/
    │   ├── login_view.py
    │   ├── admin_view.py
    │   ├── mahasiswa_view.py
    │   ├── buku_view.py
    │   ├── mhs_view.py
    │   ├── pinjam_view.py
    │   ├── kembali_view.py
    │   └── laporan_view.py
    ├── assets/
    │   ├── app.ico
    │   └── app.png
    ├── build_win.bat
    ├── build_linux.sh
    └── backend_smoke_test.py
```

---

### ▶️ Cara Menjalankan Aplikasi (Development)

```bash
# aktifkan virtualenv
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# install library
pip install -r requirements.txt

# jalankan aplikasi
python app.py
```

---

### 💻 Build Versi Kompilasi

#### 🐧 Linux

```bash
bash build_linux.sh
# hasil: dist/PerpustakaanApp/PerpustakaanApp
```

#### 🪟 Windows

```cmd
build_win.bat
# hasil: dist\PerpustakaanApp\PerpustakaanApp.exe
```

---

### 🗂️ Catatan Tambahan

- Database (`library.db`) dibuat otomatis saat program dijalankan.
- Semua commit dan branch fitur dapat dilihat di tab **Branches** / **Pull Requests** (GitHub).
- Branch tidak dihapus agar dapat dilihat dosen sebagai bukti kontribusi tiap anggota.

---

Kalau kamu mau, aku bisa tambahkan **bagian ke-5 (fitur laporan & dokumentasi)** langsung di bawah tabel anggota (biar README final kamu lengkap semua anggota).
Mau sekalian aku tambahkan sekarang?
