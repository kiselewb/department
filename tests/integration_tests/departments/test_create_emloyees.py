from httpx import AsyncClient


async def test_create_employee_success(client: AsyncClient):
    department = await client.post("/api/v1/departments/", json={"name": "IT"})
    department_id = department.json()["id"]

    response = await client.post(
        f"/api/v1/departments/{department_id}/employees/",
        json={"full_name": "Иван Иванов", "position": "Developer"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Иван Иванов"
    assert data["position"] == "Developer"
    assert data["department_id"] == department_id
    assert data["hired_at"] is None
    assert "id" in data
    assert "created_at" in data


async def test_create_employee_with_hired_at(client: AsyncClient):
    department = await client.post("/api/v1/departments/", json={"name": "IT"})
    department_id = department.json()["id"]

    response = await client.post(
        f"/api/v1/departments/{department_id}/employees/",
        json={
            "full_name": "Иван Иванов",
            "position": "Developer",
            "hired_at": "2024-01-15",
        },
    )
    assert response.status_code == 200
    assert response.json()["hired_at"] == "2024-01-15"


async def test_create_employee_nonexistent_department(client: AsyncClient):
    response = await client.post(
        "/api/v1/departments/99999/employees/",
        json={"full_name": "Иван Иванов", "position": "Developer"},
    )
    assert response.status_code == 404


async def test_create_employee_empty_full_name(client: AsyncClient):
    department = await client.post("/api/v1/departments/", json={"name": "IT"})
    department_id = department.json()["id"]

    response = await client.post(
        f"/api/v1/departments/{department_id}/employees/",
        json={"full_name": "", "position": "Developer"},
    )
    assert response.status_code == 422


async def test_create_employee_whitespace_full_name(client: AsyncClient):
    department = await client.post("/api/v1/departments/", json={"name": "IT"})
    department_id = department.json()["id"]

    response = await client.post(
        f"/api/v1/departments/{department_id}/employees/",
        json={"full_name": "   ", "position": "Developer"},
    )
    assert response.status_code == 422


async def test_create_employee_empty_position(client: AsyncClient):
    department = await client.post("/api/v1/departments/", json={"name": "IT"})
    department_id = department.json()["id"]

    response = await client.post(
        f"/api/v1/departments/{department_id}/employees/",
        json={"full_name": "Иван Иванов", "position": ""},
    )
    assert response.status_code == 422
