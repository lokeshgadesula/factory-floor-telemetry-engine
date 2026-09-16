# Factory Floor Workflow Digitization & Machine Telemetry Engine

Full-stack portfolio reference implementation for shop-floor workflow capture and live telemetry.

## Features
- FastAPI typed cycle-time, downtime, and quality events
- WebSocket live supervisor event stream
- React/TypeScript tablet UI
- Offline-first localStorage event queue and reconnect replay
- PostgreSQL Docker service boundary
- Backend tests and GitHub Actions

```text
Tablet -> REST / offline queue -> FastAPI -> PostgreSQL
                              \-> WebSocket -> Supervisor view
```

## Backend
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
uvicorn factory_engine.app:app --reload
pytest -q
```

## Frontend
```bash
cd frontend && npm install && npm run dev
```
