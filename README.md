# Cinema Ticket Booking Application

Aplikasi pemesanan tiket bioskop berbasis web dengan backend FastAPI dan frontend Vue 3.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0, PostgreSQL (Supabase)
- **Frontend**: Vue 3 (Composition API), Vite, Pinia, Vue Router, TailwindCSS

---

## Alur Pemesanan (User Flow)

Sistem dirancang dengan alur yang ringkas dan intuitif:
1. **Pilih Film**: Memilih film yang sedang aktif tayang dan menentukan jadwal tayang (studio, tanggal, jam).
2. **Pilih Kursi**: Memilih kursi pada grid studio yang terhubung langsung dengan ketersediaan kursi di database.
3. **Pembayaran**: Mengisi data pemesan singkat dan memilih metode pembayaran (Transfer Bank, E-Wallet, Kartu). Setelah dikonfirmasi, sistem langsung menerbitkan kode booking resmi.

---

## Concurrency & Data Consistency

Untuk mencegah *double-booking* kursi ketika beberapa pengguna memesan kursi yang sama secara bersamaan:
1. **Database Constraint**: Tabel `order_items` menerapkan constraint unik gabungan `(showtime_id, seat_id)`.
2. **Atomic Transaction**: Jika terjadi konflik pesanan pada kursi yang sama, transaksi di-rollback dan API merespons dengan HTTP `409 Conflict`.
3. **Holding Time**: Kursi di-hold saat pembuatan order dan otomatis kadaluarsa jika tidak dibayar dalam batas waktu yang ditentukan.

---

## Cara Menjalankan

### 1. Backend

```bash
cd backend
python -m venv venv

# Aktivasi virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Jalankan server
uvicorn app.main:app --reload --port 8000
```
API docs tersedia di `http://localhost:8000/docs`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```
Aplikasi dapat diakses di browser melalui `http://localhost:5173/` (atau `http://localhost:5174/`).

---

## Endpoint API Utama

- `GET /api/movies/`: Daftar film yang aktif.
- `GET /api/movies/{id}`: Detail film beserta jadwal tayang.
- `GET /api/showtimes/{id}/seats`: Layout kursi dan status kursi (`available` / `taken`).
- `POST /api/orders/`: Membuat pesanan dan menahan kursi.
- `POST /api/orders/{id}/pay`: Memproses pembayaran order.
