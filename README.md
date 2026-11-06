# TenderTruck

TenderTruck is a modular monolith for managing tender-based freight transportation.

## Windows 11 setup

Prerequisites: Docker Desktop with WSL 2, Git, and Python 3.12.

1. Clone and enter the repository:
   ```powershell
   git clone https://github.com/Deathbringer06/TenderTruck.git
   cd TenderTruck
   ```
2. Copy the environment template:
   ```powershell
   Copy-Item .env.example .env
   ```
3. Start PostgreSQL and the API:
   ```powershell
   docker compose up -d --build
   ```
4. Apply database migrations:
   ```powershell
   docker compose exec backend alembic upgrade head
   ```
5. Open the API documentation at `http://localhost:8000/docs`.

## Local backend tests

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
ruff check .
```
