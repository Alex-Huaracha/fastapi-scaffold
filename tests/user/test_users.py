import uuid

from httpx import AsyncClient

PAYLOAD = {
    "username": "testuser",
    "email": "TestUser@Example.COM",
    "password": "testpassword",
    "name": "Test",
    "last_name": "User",
}


async def create_user(client: AsyncClient, **overrides) -> dict:
    response = await client.post("/users", json={**PAYLOAD, **overrides})
    assert response.status_code == 201, response.text
    return response.json()


async def test_create_user_normalizes_email_and_hides_password(client: AsyncClient):
    body = await create_user(client)

    assert body["email"] == "testuser@example.com"
    assert "password" not in body


async def test_create_user_rejects_duplicate_email(client: AsyncClient):
    await create_user(client)

    response = await client.post("/users", json={**PAYLOAD, "username": "other"})

    assert response.status_code == 409


async def test_create_user_rejects_duplicate_username(client: AsyncClient):
    await create_user(client)

    response = await client.post(
        "/users", json={**PAYLOAD, "email": "other@example.com"}
    )

    assert response.status_code == 409


async def test_read_user_returns_the_user(client: AsyncClient):
    created = await create_user(client)

    response = await client.get(f"/users/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


async def test_read_user_returns_404_when_missing(client: AsyncClient):
    response = await client.get(f"/users/{uuid.uuid4()}")

    assert response.status_code == 404


async def test_update_user_changes_only_sent_fields(client: AsyncClient):
    created = await create_user(client)

    response = await client.patch(f"/users/{created['id']}", json={"name": "Renamed"})

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Renamed"
    assert body["last_name"] == created["last_name"]
    assert body["email"] == created["email"]


async def test_update_user_rejects_short_name(client: AsyncClient):
    created = await create_user(client)

    response = await client.patch(f"/users/{created['id']}", json={"name": "a"})

    assert response.status_code == 422


async def test_delete_user_removes_it(client: AsyncClient):
    created = await create_user(client)

    response = await client.delete(f"/users/{created['id']}")

    assert response.status_code == 204
    assert (await client.get(f"/users/{created['id']}")).status_code == 404


async def test_list_users_starts_empty(client: AsyncClient):
    response = await client.get("/users")

    assert response.status_code == 200
    assert response.json() == {"data": [], "total": 0, "offset": 0, "limit": 100}


async def test_list_users_paginates(client: AsyncClient):
    await create_user(client, username="ana", email="ana@example.com", name="Ana")
    await create_user(client, username="beto", email="beto@example.com", name="Beto")
    await create_user(client, username="carla", email="carla@example.com", name="Carla")

    response = await client.get("/users?offset=1&limit=1")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert [user["name"] for user in body["data"]] == ["Beto"]


async def test_list_users_orders_by_name(client: AsyncClient):
    await create_user(client, username="carla", email="carla@example.com", name="Carla")
    await create_user(client, username="ana", email="ana@example.com", name="Ana")

    response = await client.get("/users")

    assert [user["name"] for user in response.json()["data"]] == ["Ana", "Carla"]


async def test_list_users_rejects_limit_above_cap(client: AsyncClient):
    response = await client.get("/users?limit=999")

    assert response.status_code == 422
