# 📚 `littleLibrary` — Personal Book Tracker API (a lá Goodreads)

A minimalist backend API for tracking books you've read, are reading, or want to read — built with **FastAPI**, **SQLModel**, **pytest**, and other modern Python tools.

---

## 📁 Tentative Project Structure

```
readinglist/
├── app/
│   ├── main.py              # FastAPI app entrypoint
│   ├── models.py            # SQLModel database models
│   ├── schemas.py           # Pydantic request/response models
│   ├── routes.py            # API route definitions
│   ├── services.py          # DB-access functions (create/update/delete)
│   └── database.py          # DB engine and session setup
├── tests/
│   ├── conftest.py          # Fixtures
│   ├── test_routes.py       # Route/integration tests
│   └── test_services.py         # Unit tests for CRUD logic
├── requirements.txt         # Dependencies
├── README.md                # Project overview and usage
├── .env.example             # Example env vars (optional)
└── Makefile (optional)      # Dev tasks (test, run, lint)
```

---

## 🧱 Tech Stack

| Layer           | Tool                    |
| --------------- | ----------------------- |
| Web Framework   | FastAPI                 |
| ORM             | SQLModel                |
| Validation      | Pydantic                |
| DB              | SQLite (for dev)        |
| Testing         | pytest                  |
| Auth (Optional) | API key or simple token |

---

## 🧰 Suggested Features

| Feature          | Description                                                        |
| ---------------- | ------------------------------------------------------------------ |
| Add a book       | `POST /books` — title, author, status, optional notes              |
| List books       | `GET /books` — filter by status (`to_read`, `reading`, `finished`) |
| Update a book    | `PATCH /books/{id}` — change status or notes                       |
| Delete a book    | `DELETE /books/{id}`                                               |
| Full-text search | Optional: search by title or author                                |
| Pagination       | `?limit=10&offset=20`                                              |
| Testing          | Coverage for routes, schema validation, DB ops                     |
| Documentation    | FastAPI auto-generated `/docs`                                     |
| README           | With curl/Postman examples, dev setup, goals                       |
| Optional auth    | Require token in headers (e.g., `X-API-Key`)                       |

---

## 🧪 Test Strategy

* Use `pytest` with fixtures to test:

  * Model creation and validation (`BookCreate`, `BookUpdate`)
  * CRUD logic (separate from FastAPI routes)
  * Route behavior (status codes, filtering, bad inputs)
* Add a few edge cases: invalid data, missing fields, unknown IDs

---

## 📄 Example API Contract

### `POST /books`

```json
{
  "title": "The Idea of History",
  "author": "R.G. Collingwood",
  "status": "to_read",
  "notes": "Recommended by my mentor"
}
```

### `GET /books?status=reading`

Returns:

```json
[
  {
    "id": 3,
    "title": "Theory of Literature",
    "author": "Rene Wellek",
    "status": "reading",
    "notes": "Skimming chapter 4",
    "created_at": "2025-07-13T14:12:00Z",
    "updated_at": "2025-07-16T14:12:00Z"
  }
]
```

---

## 🚀 Setup Instructions

```bash
# Clone and install
git clone https://github.com/djtrack16/little_library.git
cd little_library
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload

# Run tests
pytest
```

---

## 🧼 Stretch Goals (Optional but Impressive)

* Add OpenAPI tags for route grouping
* Token-based auth via API key
* Export books to JSON or CSV
* Dockerfile or `docker-compose.yml`
* Deploy to Render/Fly.io for public demo
