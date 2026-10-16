# Cinema Ticket Booking System

Aplikasi pemesanan tiket bioskop sederhana dengan fokus pada validasi data dan penanganan *concurrency* di sisi backend.

- **Backend**: FastAPI, SQLAlchemy 2.0, PostgreSQL (Supabase Cloud)
- **Frontend**: Vue 3, Vite, TailwindCSS

---

## Substansi Teknis & Concurrency

Tantangan utama sistem pemesanan tiket adalah mencegah **double-booking** (dua pengguna memesan kursi yang sama secara bersamaan). Sistem ini menanganinya melalui:

1. **Database Constraint**:  
   Tabel `order_items` menerapkan `UniqueConstraint("showtime_id", "seat_id")`.
2. **Atomic Rollback & Status 409**:  
   Jika terjadi bentrokan saat transaksi disimpan, database menolak operasi tersebut dan FastAPI me-rollback transaksi lalu mengembalikan status `HTTP 409 Conflict`.
3. **Mekanisme Hold Timeout (10 Menit)**:  
   Ketika order dibuat, status order adalah `pending` selama 10 menit. Jika tidak diselesaikan pembayarannya, kursi otomatis dirilis kembali untuk penonton lain.

---

## Cara Menjalankan

> **Catatan Database**: Proyek ini sudah terhubung ke database **PostgreSQL di Supabase Cloud**. Anda **tidak perlu menginstall atau membuat database PostgreSQL lokal**.

### 1. Jalankan Backend

```bash
cd backend

# Buat & aktifkan virtual environment (opsional tapi direkomendasikan)
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Pastikan file .env ada (sudah disediakan default koneksi Supabase)
# Jika belum ada, salin dari .env.example:
cp .env.example .env

# Jalankan server API
uvicorn app.main:app --reload --port 8000
```
API docs (Swagger) aktif di `http://localhost:8000/docs`.

---

### 2. Jalankan Frontend

```bash
cd frontend

# Install dependencies & jalankan dev server
npm install
npm run dev
```
Buka browser di `http://localhost:5173/` (atau `http://localhost:5174/`).

---

## Endpoint API

| Method | Endpoint | Fungsi |
|---|---|---|
| `GET` | `/api/movies/` | Mengambil daftar film aktif beserta jadwal penayangan |
| `GET` | `/api/showtimes/{id}/seats` | Mengambil 5 kursi studio beserta status (`available` / `taken`) |
| `POST` | `/api/orders/` | Membuat pesanan baru & menahan kursi (hold) |
| `POST` | `/api/orders/{id}/pay` | Eksekusi pembayaran (`qris` / `bca`) |
