from httpx import AsyncClient


async def test_get_department_success(client: AsyncClient):
    department = await client.post("/api/v1/departments/", json={"name": "IT"})
    department_id = department.json()["id"]

    response = await client.get(f"/api/v1/departments/{department_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == department_id
    assert data["name"] == "IT"
    assert data["children"] == []
    assert data["employees"] == []


async def test_get_department_not_found(client: AsyncClient):
    response = await client.get("/api/v1/departments/99999")
    assert response.status_code == 404


async def test_get_department_with_children(client: AsyncClient):
    parent = await client.post("/api/v1/departments/", json={"name": "IT"})
    parent_id = parent.json()["id"]

    await client.post(
        "/api/v1/departments/", json={"name": "Backend", "parent_id": parent_id}
    )
    await client.post(
        "/api/v1/departments/", json={"name": "Frontend", "parent_id": parent_id}
    )

    response = await client.get(f"/api/v1/departments/{parent_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["children"]) == 2
    children_names = [c["name"] for c in data["children"]]
    assert "Backend" in children_names
    assert "Frontend" in children_names


async def test_get_department_with_employees(client: AsyncClient):
    department = await client.post("/api/v1/departments/", json={"name": "IT"})
    department_id = department.json()["id"]

    await client.post(
        f"/api/v1/departments/{department_id}/employees/",
        json={"full_name": "Иван Иванов", "position": "Developer"},
    )

    response = await client.get(f"/api/v1/departments/{department_id}")
    assert response.status_code == 200
    assert len(response.json()["employees"]) == 1
    assert response.json()["employees"][0]["full_name"] == "Иван Иванов"


async def test_get_department_exclude_employees(client: AsyncClient):
    department = await client.post("/api/v1/departments/", json={"name": "IT"})
    department_id = department.json()["id"]

    await client.post(
        f"/api/v1/departments/{department_id}/employees/",
        json={"full_name": "Иван Иванов", "position": "Developer"},
    )

    response = await client.get(
        f"/api/v1/departments/{department_id}", params={"include_employees": False}
    )
    assert response.status_code == 200
    assert response.json()["employees"] == []


async def test_get_department_depth(client: AsyncClient):
    a = await client.post("/api/v1/departments/", json={"name": "A"})
    a_id = a.json()["id"]
    b = await client.post("/api/v1/departments/", json={"name": "B", "parent_id": a_id})
    b_id = b.json()["id"]
    c = await client.post("/api/v1/departments/", json={"name": "C", "parent_id": b_id})
    c_id = c.json()["id"]
    await client.post("/api/v1/departments/", json={"name": "D", "parent_id": c_id})

    response = await client.get(f"/api/v1/departments/{a_id}", params={"depth": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data["children"]) == 1
    assert len(data["children"][0]["children"]) == 1
    assert data["children"][0]["children"][0]["children"] == []


async def test_get_department_depth_max(client: AsyncClient):
    department = await client.post("/api/v1/departments/", json={"name": "IT"})
    department_id = department.json()["id"]

    response = await client.get(
        f"/api/v1/departments/{department_id}", params={"depth": 6}
    )
    assert response.status_code == 422


async def test_get_department_employees_in_children(client: AsyncClient):
    parent = await client.post("/api/v1/departments/", json={"name": "IT"})
    parent_id = parent.json()["id"]

    child = await client.post(
        "/api/v1/departments/", json={"name": "Backend", "parent_id": parent_id}
    )
    child_id = child.json()["id"]

    await client.post(
        f"/api/v1/departments/{child_id}/employees/",
        json={"full_name": "Иван Иванов", "position": "Developer"},
    )

    response = await client.get(f"/api/v1/departments/{parent_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["employees"] == []
    assert len(data["children"][0]["employees"]) == 1
