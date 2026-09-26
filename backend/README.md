# Minor Backend

FastAPI + SQLAlchemy backend for the mid-term MLOps monitoring demo.

Run:
1. Copy `.env.example` to `.env`.
2. Put the Supabase PostgreSQL connection string in `DATABASE_URL`.
3. `pip install -r requirements.txt`
4. `uvicorn backend.app:app --reload`

Endpoints:
- `GET /health`
- `POST /api/v1/production`
- `GET /api/v1/drift`
- `GET /api/v1/history`

The production endpoint currently inserts demo monitoring values until the ML integration is connected.
