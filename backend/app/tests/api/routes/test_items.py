from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models import Vehicle
from app.tests.utils.vehicle import create_random_vehicle


def test_create_vehicle(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/vehicles/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_vehicle(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    vehicle: Vehicle = create_random_vehicle(db)
    response = client.get(
        f"{settings.API_V1_STR}/vehicles/{vehicle.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["vin"] == vehicle.vin
    assert content["id"] == vehicle.id
    assert content["owner_id"] == vehicle.owner_id


def test_read_vehicle_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/vehicles/999",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Vehicle not found"


def test_read_vehicle_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    vehicle: Vehicle = create_random_vehicle(db)
    response = client.get(
        f"{settings.API_V1_STR}/vehicles/{vehicle.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_vehicles(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_vehicle(db)
    create_random_vehicle(db)
    response = client.get(
        f"{settings.API_V1_STR}/vehicles/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_vehicle(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    vehicle = create_random_vehicle(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/vehicles/{vehicle.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["id"] == vehicle.id
    assert content["owner_id"] == vehicle.owner_id


def test_update_vehicle_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/vehicles/999",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Vehicle not found"


def test_update_vehicle_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    vehicle = create_random_vehicle(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/vehicles/{vehicle.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_vehicle(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    vehicle = create_random_vehicle(db)
    response = client.delete(
        f"{settings.API_V1_STR}/vehicles/{vehicle.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Vehicle deleted successfully"


def test_delete_vehicle_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/vehicles/999",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Vehicle not found"


def test_delete_vehicle_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    vehicle = create_random_vehicle(db)
    response = client.delete(
        f"{settings.API_V1_STR}/vehicles/{vehicle.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
