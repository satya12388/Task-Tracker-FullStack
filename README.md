# 🚀 Full-Stack Task Manager (FastAPI + Streamlit + SQLAlchemy)

An educational, beginner-friendly full-stack application demonstrating how to build, connect, and structure a modern Python backend and frontend.

---

## 📖 Overview (In Simple Terms)

Think of this project as a complete **three-tier web application** written entirely in Python:

1. **The User Interface (Frontend):** Built with **[Streamlit](https://streamlit.io/)**, providing a clean web dashboard with progress bars, metrics, task lists, and forms to add, edit, toggle, or delete tasks.
2. **The Logic & Communication Layer (Backend API):** Built with **[FastAPI](https://fastapi.tiangolo.com/)**, receiving requests from the frontend, enforcing data validation rules, and directing operations.
3. **The Storage Layer (Database):** Built with **[SQLite](https://www.sqlite.org/)** and managed through **[SQLAlchemy 2.0](https://www.sqlalchemy.org/)**, reliably saving and retrieving tasks on disk.

```
┌─────────────────────────┐          HTTP / JSON          ┌─────────────────────────┐
│     Streamlit UI        │ ◄───────────────────────────► │      FastAPI App        │
│   (Frontend/UIapp.py)   │    POST / GET / PUT / DELETE  │    (Backend/app.py)     │
└─────────────────────────┘                               └───────────┬─────────────┘
                                                                      │
                                                           SQLAlchemy │ ORM Sessions
                                                                      ▼
                                                          ┌─────────────────────────┐
                                                          │     SQLite Database     │
                                                          │       (tasks.db)        │
                                                          └─────────────────────────┘
```

---

## 🎯 What This Project Demonstrates

This repository is designed to teach essential full-stack Python concepts in an approachable way:

### 1. RESTful API Architecture
- Follows standard HTTP methods:
  - `GET` to read data (`/api/v1/Tasks`, `/api/v1/Task/{id}`)
  - `POST` to create resources (`/api/v1/Tasks`)
  - `PUT` to update existing resources (`/api/v1/Task/{id}`)
  - `DELETE` to remove resources (`/api/v1/Task/{id}`)
- Uses clear URL versioning (`/api/v1/...`).

### 2. Modern Data Validation with Pydantic v2
- Separates **input schemas** from **output schemas**:
  - `createTask`: Used when adding a new task (does not include an ID, since the database generates it).
  - `Task`: Used when returning existing tasks (includes `id`, `name`, `description`, `is_completed`).
- `ConfigDict(from_attributes=True)`: Allows Pydantic to read data directly from SQLAlchemy database objects without manual dictionary conversion.

### 3. Modern SQLAlchemy 2.0 ORM
- Uses modern Type Annotations (`Mapped[int]`, `Mapped[str]`, `mapped_column`) instead of legacy SQLAlchemy 1.x syntax.
- Manages database transactions and connection lifetimes cleanly via Python generators (`yield db`) and FastAPI's `Depends(get_db)`.

### 4. Interactive Python Frontend with Streamlit
- Demonstrates server healthchecks (alerts the user if the backend is down).
- Live KPI metrics (Total Tasks, Completed, Pending, and Completion Percentage).
- In-place task editing and completion toggling using Streamlit session state and forms.

### 5. Automatic Interactive API Documentation
- FastAPI automatically provides interactive **Swagger UI** (`/docs`) and **ReDoc** (`/redoc`) out of the box with zero manual documentation writing.

---

## 📂 Project Structure

```text
FAST_API/
├── Backend/
│   ├── database/
│   │   ├── database.py       # Engine, sessionmaker, and get_db dependency
│   │   └── models.py         # SQLAlchemy DB models (DBTask table definition)
│   ├── routes/
│   │   └── taskroutes.py     # API endpoints (GET, POST, PUT, DELETE)
│   ├── app.py                # FastAPI application entrypoint & router inclusion
│   ├── schemas.py            # Pydantic data validation schemas
│   └── __init__.py
├── Frontend/
│   └── UIapp.py              # Streamlit dashboard interface
├── dummy_data.py             # Sample mock data for testing or seeding
├── pyproject.toml            # Project dependencies and metadata
├── uv.lock                   # Deterministic lockfile for reproducible installs
├── .gitignore                # Git ignore rules (protects secrets and database files)
└── README.md                 # Project documentation
```

---

## 🛠️ Prerequisites

- **Python 3.12+**
- Recommended package manager: **[uv](https://docs.astral.sh/uv/)** (or standard `pip` / `venv`)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Set Up a Virtual Environment

#### Option A: Using `uv` (Recommended - Fast)
```bash
# uv creates and manages the virtual environment automatically:
uv sync
```

#### Option B: Using standard Python `venv`
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install fastapi[standard] streamlit sqlalchemy requests
```

---

## 🏃 Running the Application

You need two terminal windows: one for the **Backend** and one for the **Frontend**.

### Step 1: Start the Backend (FastAPI)
In your first terminal, run:
```bash
uvicorn Backend.app:app --reload --port 8000
```
- The API will be available at: `http://127.0.0.1:8000`
- Interactive Swagger documentation: **`http://127.0.0.1:8000/docs`**
- Alternative ReDoc documentation: **`http://127.0.0.1:8000/redoc`**

### Step 2: Start the Frontend (Streamlit)
In your second terminal, run:
```bash
streamlit run Frontend/UIapp.py
```
- The web browser will automatically open at: `http://localhost:8501`

---

## 📡 API Reference

All routes are prefixed with `/api/v1`:

| Method | Endpoint | Description | Request Body | Response Code |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/home` | Healthcheck / status check | None | `200 OK` |
| `GET` | `/Tasks` | Fetch all tasks | None | `200 OK` |
| `GET` | `/Task/{id}` | Fetch a single task by ID | None | `200 OK` / `404 Not Found` |
| `POST` | `/Tasks` | Create a new task | JSON (`name`, `description`, `is_completed`) | `200 OK` |
| `PUT` | `/Task/{id}` | Update an existing task | JSON (`name`, `description`, `is_completed`) | `201 Created` / `404 Not Found` |
| `DELETE` | `/Task/{id}` | Delete a task | None | `200 OK` / `404 Not Found` |

---

## 🔒 Security & Best Practices (For Learning & Production)

Because this repository is intended for **educational purposes**, here are important real-world security practices to keep in mind when moving from learning to production:

1. **Keep Database Files Out of Git:**
   - The `.gitignore` in this project is configured to ignore `*.db` and `*.sqlite3`. Never commit local database files, as they can leak test records or bloat your git history.
2. **Environment Variables:**
   - Avoid hardcoding configuration URLs (such as `http://127.0.0.1:8000`) or database paths. In production, use `python-dotenv` or `pydantic-settings` to load values from `.env` files.
3. **CORS (Cross-Origin Resource Sharing):**
   - If connecting a web browser frontend (e.g. React, Vue, or Angular) running on another domain, configure FastAPI's `CORSMiddleware` with explicit allowed origins rather than wildcard `*`.
4. **Input Length Validation:**
   - Database columns have string limits (e.g., `String(50)`). Pydantic schemas should enforce matching `max_length` constraints to prevent database error exceptions.
5. **SQL Injection Protection:**
   - This project uses SQLAlchemy ORM query methods (`db.get()`, `select()`), which automatically parameterize SQL queries and defend against SQL injection. Avoid writing raw SQL with string concatenation (`f"SELECT * FROM tasks WHERE id = {id}"`).

---

## 📝 License

This project is licensed under the [MIT License](LICENSE) — free to use for educational, personal, or commercial purposes.

