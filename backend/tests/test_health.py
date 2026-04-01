def test_health_endpoint_returns_ok(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_root_endpoint_exposes_docs_link(client):
    response = client.get("/api")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["docs"] == "/docs"
