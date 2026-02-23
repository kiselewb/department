from httpx import AsyncClient


async def test_create_department_success(client: AsyncClient):
    response = await client.post("/api/v1/departments/", json={"name": "IT"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "IT"
    assert data["parent_id"] is None
    assert "id" in data
    assert "created_at" in data


async def test_create_department_with_parent(client: AsyncClient):
    parent = await client.post("/api/v1/departments/", json={"name": "IT"})
    parent_id = parent.json()["id"]

    response = await client.post(
        "/api/v1/departments/", json={"name": "Backend", "parent_id": parent_id}
    )
    assert response.status_code == 200
    assert response.json()["parent_id"] == parent_id


async def test_create_department_duplicate_name_same_parent(client: AsyncClient):
    parent = await client.post("/api/v1/departments/", json={"name": "IT"})
    parent_id = parent.json()["id"]

    await client.post(
        "/api/v1/departments/", json={"name": "Backend", "parent_id": parent_id}
    )
    response = await client.post(
        "/api/v1/departments/", json={"name": "Backend", "parent_id": parent_id}
    )
    assert response.status_code == 409


async def test_create_department_duplicate_name_different_parent(client: AsyncClient):
    parent1 = await client.post("/api/v1/departments/", json={"name": "IT"})
    parent2 = await client.post("/api/v1/departments/", json={"name": "HR"})

    await client.post(
        "/api/v1/departments/",
        json={"name": "Backend", "parent_id": parent1.json()["id"]},
    )
    response = await client.post(
        "/api/v1/departments/",
        json={"name": "Backend", "parent_id": parent2.json()["id"]},
    )
    assert response.status_code == 200


async def test_create_department_nonexistent_parent(client: AsyncClient):
    response = await client.post(
        "/api/v1/departments/", json={"name": "IT", "parent_id": 99999}
    )
    assert response.status_code == 404


async def test_create_department_empty_name(client: AsyncClient):
    response = await client.post("/api/v1/departments/", json={"name": ""})
    assert response.status_code == 422


async def test_create_department_whitespace_name(client: AsyncClient):
    response = await client.post("/api/v1/departments/", json={"name": "   "})
    assert response.status_code == 422


async def test_create_department_name_trimmed(client: AsyncClient):
    response = await client.post("/api/v1/departments/", json={"name": "  IT  "})
    assert response.status_code == 200
    assert response.json()["name"] == "IT"
