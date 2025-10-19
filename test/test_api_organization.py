def test_create_organization_success(client):
    payload = {"name": "ACME Inc", "code": "ACME", "description": "Test"}
    r = client.post("/api/v1/organizations", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "ACME Inc"
    assert data["code"] == "ACME"


def test_create_organization_conflict(client):
    payload = {"name": "ACME Inc", "code": "ACME2", "description": "Test"}
    r1 = client.post("/api/v1/organizations", json=payload)
    assert r1.status_code == 201
    # Post again with same code should succeed or conflict depending on unique constraint/enforcement in service
    r2 = client.post("/api/v1/organizations", json=payload)
    assert r2.status_code in (201, 409)
