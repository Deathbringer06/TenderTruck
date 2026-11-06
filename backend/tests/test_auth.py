from fastapi.testclient import TestClient

from src.app.db.base import Base
from src.app.db.engine import engine
from src.main import app


def setup_module() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_health() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}
