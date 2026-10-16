# Cinema Ticket Booking

A fullstack cinema ticket booking application built with FastAPI and Vue 3.

> **Note:** The application is already connected to a hosted PostgreSQL database on Supabase Cloud. No local database installation is required.

---

## Getting Started

### 1. Backend (FastAPI)

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Ensure .env is present (already pre-configured with Supabase Cloud DB)
# If missing, copy from example:
cp .env.example .env

# Run the API server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.  
Interactive API documentation (Swagger UI): `http://localhost:8000/docs`.

---

### 2. Frontend (Vue 3)

Open a new terminal window:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Open your browser at `http://localhost:5173/` (or `http://localhost:5174/`).

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/movies/` | List all active movies and schedules |
| `GET` | `/api/showtimes/{id}/seats` | Get seat layout and availability status |
| `POST` | `/api/orders/` | Create a booking order (hold seats) |
| `POST` | `/api/orders/{id}/pay` | Process payment (`qris` or `bca`) |
