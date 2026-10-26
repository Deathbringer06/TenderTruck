import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.api import deps
from app.database import Base
from app.main import app


@pytest.fixture()
def client(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[deps.get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def registration_payload(email="user@example.com", phone="+996700000001", inn="123456789012"):
    return {
        "email": email,
        "phone": phone,
        "password": "StrongPassword123!",
        "role": "zakazchik",
        "inn": inn,
    }


def test_register_and_duplicate_email(client):
    response = client.post("/api/v1/auth/register", json=registration_payload())
    assert response.status_code == 201
    assert response.json()["email"] == "user@example.com"

    duplicate = client.post("/api/v1/auth/register", json=registration_payload(inn="987654321098"))
    assert duplicate.status_code == 400


def test_login_success_and_failure(client):
    client.post("/api/v1/auth/register", json=registration_payload())
    login = client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "StrongPassword123!"})
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"

    failure = client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "wrong"})
    assert failure.status_code == 401
    assert failure.json() == {"detail": "Неверный email или пароль"}


def test_profile_requires_token_and_can_be_updated(client):
    assert client.get("/api/v1/users/me").status_code == 401
    client.post("/api/v1/auth/register", json=registration_payload())
    token = client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "StrongPassword123!"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    profile = client.get("/api/v1/users/me", headers=headers)
    assert profile.status_code == 200
    assert set(profile.json()) == {"id", "email", "phone", "role", "inn", "is_verified", "company_name", "description", "contact_person", "address"}

    updated = client.put(
        "/api/v1/users/me",
        headers=headers,
        json={"company_name": "Tender Truck", "description": "Описание", "contact_person": "Иван", "phone": "+996700000002", "address": "Бишкек"},
    )
    assert updated.status_code == 200
    assert updated.json()["company_name"] == "Tender Truck"
    assert updated.json()["phone"] == "+996700000002"


def test_duplicate_phone_on_profile_update(client):
    client.post("/api/v1/auth/register", json=registration_payload())
    client.post("/api/v1/auth/register", json=registration_payload(email="other@example.com", phone="+996700000002", inn="987654321098"))
    token = client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "StrongPassword123!"}).json()["access_token"]
    response = client.put("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}, json={"phone": "+996700000002"})
    assert response.status_code == 400
