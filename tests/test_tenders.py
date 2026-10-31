from datetime import datetime, timedelta

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
    engine = create_engine(f"sqlite:///{tmp_path / 'tenders.db'}", connect_args={"check_same_thread": False})
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[deps.get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def users(client):
    result = {}
    for role, suffix in (("zakazchik", "customer"), ("perevozchik", "carrier"), ("zakazchik", "other")):
        email = f"{suffix}@example.com"
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "phone": f"+9967000000{len(result) + 1:02}",
                "password": "StrongPassword123!",
                "role": role,
                "inn": f"1234567890{len(result) + 1:02}",
            },
        )
        assert response.status_code == 201
        token = client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": "StrongPassword123!"},
        ).json()["access_token"]
        result[suffix] = {"Authorization": f"Bearer {token}"}
    return result


def tender_payload(**changes):
    payload = {
        "point_a": "Бишкек",
        "point_b": "Ош",
        "cargo_weight": 1200.5,
        "cargo_volume": 12.5,
        "body_type": "тент",
        "loading_date": (datetime.utcnow() + timedelta(days=3)).isoformat(),
        "unloading_date": (datetime.utcnow() + timedelta(days=4)).isoformat(),
        "start_price": 50000,
    }
    return {**payload, **changes}


def create_tender(client, headers, **changes):
    return client.post("/api/v1/tenders", headers=headers, json=tender_payload(**changes))


def test_create_tender_as_customer(client, users):
    response = create_tender(client, users["customer"])
    assert response.status_code == 201
    assert response.json()["point_a"] == "Бишкек"
    assert response.json()["start_price"] == 50000
    assert response.json()["status"] == "open"


def test_create_tender_as_carrier_forbidden(client, users):
    assert create_tender(client, users["carrier"]).status_code == 403


def test_get_my_tenders_returns_only_own(client, users):
    create_tender(client, users["customer"])
    create_tender(client, users["other"], point_a="Талас")
    response = client.get("/api/v1/tenders/my", headers=users["customer"])
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["point_a"] == "Бишкек"


def test_get_open_tenders_as_carrier(client, users):
    created = create_tender(client, users["customer"]).json()
    client.patch(
        f"/api/v1/tenders/{created['id']}",
        headers=users["customer"],
        json={"status": "closed"},
    )
    create_tender(client, users["other"])
    response = client.get("/api/v1/tenders/open", headers=users["carrier"])
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "open"


def test_get_open_tenders_as_customer_forbidden(client, users):
    assert client.get("/api/v1/tenders/open", headers=users["customer"]).status_code == 403


def test_get_tender_detail_as_carrier(client, users):
    created = create_tender(client, users["customer"]).json()
    response = client.get(f"/api/v1/tenders/{created['id']}", headers=users["carrier"])
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_tender_detail_not_found(client, users):
    assert client.get("/api/v1/tenders/999", headers=users["carrier"]).status_code == 404


def test_patch_tender_by_owner(client, users):
    created = create_tender(client, users["customer"]).json()
    response = client.patch(
        f"/api/v1/tenders/{created['id']}",
        headers=users["customer"],
        json={"point_b": "Нарын", "start_price": 60000},
    )
    assert response.status_code == 200
    assert response.json()["point_b"] == "Нарын"
    assert response.json()["start_price"] == 60000


def test_patch_tender_not_owner_forbidden(client, users):
    created = create_tender(client, users["customer"]).json()
    response = client.patch(
        f"/api/v1/tenders/{created['id']}",
        headers=users["other"],
        json={"point_b": "Нарын"},
    )
    assert response.status_code == 403


def test_cannot_edit_closed_tender(client, users):
    created = create_tender(client, users["customer"]).json()
    client.patch(
        f"/api/v1/tenders/{created['id']}",
        headers=users["customer"],
        json={"status": "closed"},
    )
    response = client.patch(
        f"/api/v1/tenders/{created['id']}",
        headers=users["customer"],
        json={"point_b": "Нарын"},
    )
    assert response.status_code == 400


def test_delete_tender_by_owner(client, users):
    created = create_tender(client, users["customer"]).json()
    response = client.delete(f"/api/v1/tenders/{created['id']}", headers=users["customer"])
    assert response.status_code == 204
    assert client.get(f"/api/v1/tenders/{created['id']}", headers=users["carrier"]).status_code == 404


def test_delete_tender_not_owner_forbidden(client, users):
    created = create_tender(client, users["customer"]).json()
    response = client.delete(f"/api/v1/tenders/{created['id']}", headers=users["other"])
    assert response.status_code == 403
