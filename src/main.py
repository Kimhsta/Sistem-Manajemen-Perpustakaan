from database.db import init_db
from models.book_model import BookModel
from models.student_model import StudentModel
from models.loan_model import LoanModel

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
