# Sistem-Manajemen-Perpustakaan-

update

baik banget, kalo tim kamu masih pemula dan biar gampang dipahami semua anggota, kita sederhanakan jadi **struktur folder user-friendly** tapi tetap rapi dan bisa dikembangkan.
Berikut versi yang ringan, cocok untuk 5 orang mahasiswa 👇

---

## 📁 Struktur Folder Sederhana

```
PerpustakaanApp/
│
├── main.py                  # file utama, jalankan program Tkinter
│
├── database/
│   └── db.py                # koneksi & tabel SQLite
│
├── models/
│   ├── book_model.py        # kelas & fungsi buku
│   ├── student_model.py     # kelas & fungsi mahasiswa
│   └── loan_model.py        # kelas & fungsi peminjaman
│
├── views/                   # semua tampilan GUI
│   ├── login_view.py        # halaman login
│   ├── admin_view.py        # menu admin
│   ├── mahasiswa_view.py    # menu mahasiswa
│   ├── buku_view.py         # CRUD buku
│   ├── mhs_view.py          # CRUD mahasiswa
│   ├── pinjam_view.py       # peminjaman
│   ├── kembali_view.py      # pengembalian
│   └── laporan_view.py      # laporan
│
└── data/
    └── library.db           # file database SQLite
```

---

## 📋 Pembagian Tugas yang Gampang Dipahami

| Anggota                           | Tugas Utama                                        | File Fokus                                                              | Keterangan                                  |
| --------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------- |
| **1. Backend (Database)**         | Buat dan kelola tabel SQLite                       | `database/db.py`, `models/*.py`                                         | Buat fungsi tambah, hapus, edit, ambil data |
| **2. GUI Login & Menu Utama**     | Halaman login dan dashboard admin/mahasiswa        | `views/login_view.py`, `views/admin_view.py`, `views/mahasiswa_view.py` | Setelah login, arahkan sesuai role          |
| **3. CRUD Buku & Mahasiswa**      | Form tambah, edit, hapus buku dan mahasiswa        | `views/buku_view.py`, `views/mhs_view.py`                               | Gunakan `Treeview` Tkinter                  |
| **4. Peminjaman & Pengembalian**  | Fitur pinjam & kembalikan buku                     | `views/pinjam_view.py`, `views/kembali_view.py`                         | Kurangi/tambah stok otomatis, hitung denda  |
| **5. Laporan & Dokumentasi(Eka)** | Tampilan laporan & ekspor data, dokumentasi README | `views/laporan_view.py`, `README.md`                                    | Menampilkan semua transaksi dan denda       |

---

## 💡 Tips Koordinasi

1. **Gunakan GitHub** → buat repo, semua push ke branch masing-masing.
2. Semua file tampilan (`views/`) **panggil fungsi dari model**, jangan langsung query ke database.
3. Buat **1 style UI sederhana** biar tampilan mirip.
4. Simpan **library.db** di folder `data/`, jangan di-commit ke GitHub.

---

## ⚙️ Jalankan Aplikasi

```bash
python main.py
```

---

Kalau kamu mau, aku bisa bantu lanjut:

- Buatkan **versi dasar semua folder kosong + template file .py-nya** (biar tim tinggal isi),
  atau
- Langsung **buat kerangka GUI (Login + Menu Admin + Menu Mahasiswa)** yang bisa dijalankan.

Kamu mau saya bantu yang mana dulu, bang — folder kosong + template, atau langsung GUI dasarnya?
