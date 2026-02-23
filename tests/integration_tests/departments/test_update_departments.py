from httpx import AsyncClient


async def test_update_department_name(client: AsyncClient):
    department = await client.post("/api/v1/departments/", json={"name": "IT"})
    department_id = department.json()["id"]

    response = await client.patch(
        f"/api/v1/departments/{department_id}", json={"name": "IT Updated"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "IT Updated"


async def test_update_department_parent(client: AsyncClient):
    parent = await client.post("/api/v1/departments/", json={"name": "IT"})
    child = await client.post("/api/v1/departments/", json={"name": "Backend"})
    parent_id = parent.json()["id"]
    child_id = child.json()["id"]

    response = await client.patch(
        f"/api/v1/departments/{child_id}", json={"parent_id": parent_id}
    )
    assert response.status_code == 200
    assert response.json()["parent_id"] == parent_id


async def test_update_department_move_to_root(client: AsyncClient):
    parent = await client.post("/api/v1/departments/", json={"name": "IT"})
    child = await client.post(
        "/api/v1/departments/",
        json={"name": "Backend", "parent_id": parent.json()["id"]},
    )
    child_id = child.json()["id"]

    response = await client.patch(
        f"/api/v1/departments/{child_id}", json={"parent_id": None}
    )
    assert response.status_code == 200
    assert response.json()["parent_id"] is None


async def test_update_department_not_found(client: AsyncClient):
    response = await client.patch("/api/v1/departments/99999", json={"name": "IT"})
    assert response.status_code == 404


async def test_update_department_empty_body(client: AsyncClient):
    department = await client.post("/api/v1/departments/", json={"name": "IT"})
    department_id = department.json()["id"]

    response = await client.patch(f"/api/v1/departments/{department_id}", json={})
    assert response.status_code == 422


async def test_update_department_self_parent(client: AsyncClient):
    department = await client.post("/api/v1/departments/", json={"name": "IT"})
    department_id = department.json()["id"]

    response = await client.patch(
        f"/api/v1/departments/{department_id}", json={"parent_id": department_id}
    )
    assert response.status_code == 409


async def test_update_department_cycle(client: AsyncClient):
    a = await client.post("/api/v1/departments/", json={"name": "A"})
    a_id = a.json()["id"]

    b = await client.post("/api/v1/departments/", json={"name": "B", "parent_id": a_id})
    b_id = b.json()["id"]

    c = await client.post("/api/v1/departments/", json={"name": "C", "parent_id": b_id})
    c_id = c.json()["id"]

    response = await client.patch(
        f"/api/v1/departments/{a_id}", json={"parent_id": c_id}
    )
    assert response.status_code == 409


async def test_update_department_duplicate_name_same_parent(client: AsyncClient):
    parent = await client.post("/api/v1/departments/", json={"name": "IT"})
    parent_id = parent.json()["id"]

    await client.post(
        "/api/v1/departments/", json={"name": "Backend", "parent_id": parent_id}
    )
    frontend = await client.post(
        "/api/v1/departments/", json={"name": "Frontend", "parent_id": parent_id}
    )

    response = await client.patch(
        f"/api/v1/departments/{frontend.json()['id']}", json={"name": "Backend"}
    )
    assert response.status_code == 409
