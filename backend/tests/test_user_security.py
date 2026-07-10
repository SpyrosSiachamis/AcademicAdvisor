from src.modules.storage import memory

from .conftest import clear_memory, client


def setup_function():
    clear_memory()


def test_create_user_does_not_return_password_or_password_hash():
    # Create required department first if your user requires department_id
    memory.departments.append({
        "id": 1,
        "name": "Computer Science",
        "university_id": 1
    })

    response = client.post("/users/", json={
        "id": 1,
        "username": "spiros",
        "email": "spiros@example.com",
        "password": "secret123",
        "department_id": 1
    })

    assert response.status_code in (200, 201)

    data = response.json()

    assert "password" not in str(data)
    assert "password_hash" not in str(data)
    assert "secret123" not in str(data)


def test_get_user_does_not_return_password_or_password_hash(auth_headers):
    memory.departments.append({
        "id": 1,
        "name": "Computer Science",
        "university_id": 1
    })

    create_response = client.post("/users/", json={
        "id": 2,
        "username": "testuser",
        "email": "test@example.com",
        "password": "secret456",
        "department_id": 1
    })

    assert create_response.status_code in (200, 201)

    get_response = client.get("/users/2", headers=auth_headers)

    assert get_response.status_code == 200

    data = get_response.json()

    assert "password" not in str(data)
    assert "password_hash" not in str(data)
    assert "secret456" not in str(data)
