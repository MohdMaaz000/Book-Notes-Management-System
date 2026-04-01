from tests.conftest import register_user


def test_protected_routes_require_authentication(client):
    response = client.get("/api/v1/books")

    assert response.status_code == 401
    assert response.json()["message"] == "Access token is required"


def test_books_crud_and_listing(client):
    auth = register_user(client, name="Books User", email="books@example.com")

    create_response = client.post(
        "/api/v1/books",
        json={"title": "Alpha Book", "description": "First description"},
        headers=auth["headers"],
    )
    assert create_response.status_code == 201
    created_book = create_response.json()
    book_id = created_book["id"]
    assert created_book["title"] == "Alpha Book"

    get_response = client.get(f"/api/v1/books/{book_id}", headers=auth["headers"])
    assert get_response.status_code == 200
    assert get_response.json()["description"] == "First description"

    update_response = client.patch(
        f"/api/v1/books/{book_id}",
        json={"title": "Updated Book"},
        headers=auth["headers"],
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Book"

    second_book_response = client.post(
        "/api/v1/books",
        json={"title": "Zeta Book", "description": "Second description"},
        headers=auth["headers"],
    )
    assert second_book_response.status_code == 201

    list_response = client.get(
        "/api/v1/books?page=1&page_size=10&search=Book&sort_by=title&sort_order=asc",
        headers=auth["headers"],
    )
    assert list_response.status_code == 200
    payload = list_response.json()
    assert payload["meta"]["total_items"] == 2
    assert [item["title"] for item in payload["items"]] == ["Updated Book", "Zeta Book"]

    delete_response = client.delete(f"/api/v1/books/{book_id}", headers=auth["headers"])
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Book deleted successfully"

    missing_response = client.get(f"/api/v1/books/{book_id}", headers=auth["headers"])
    assert missing_response.status_code == 404
    assert missing_response.json()["message"] == "Book not found"


def test_notes_crud_and_search(client):
    auth = register_user(client, name="Notes User", email="notes@example.com")
    book_response = client.post(
        "/api/v1/books",
        json={"title": "Reference Book", "description": "For notes"},
        headers=auth["headers"],
    )
    book_id = book_response.json()["id"]

    create_response = client.post(
        f"/api/v1/books/{book_id}/notes",
        json={"title": "First Note", "content": "Important text here"},
        headers=auth["headers"],
    )
    assert create_response.status_code == 201
    created_note = create_response.json()
    note_id = created_note["id"]
    assert created_note["content"] == "Important text here"

    update_response = client.patch(
        f"/api/v1/books/{book_id}/notes/{note_id}",
        json={"content": "Updated content"},
        headers=auth["headers"],
    )
    assert update_response.status_code == 200
    assert update_response.json()["content"] == "Updated content"

    second_note_response = client.post(
        f"/api/v1/books/{book_id}/notes",
        json={"title": "Second Note", "content": "Searchable keyword"},
        headers=auth["headers"],
    )
    assert second_note_response.status_code == 201

    list_response = client.get(
        f"/api/v1/books/{book_id}/notes?search=keyword&sort_by=title&sort_order=asc",
        headers=auth["headers"],
    )
    assert list_response.status_code == 200
    payload = list_response.json()
    assert payload["meta"]["total_items"] == 1
    assert payload["items"][0]["title"] == "Second Note"

    delete_response = client.delete(
        f"/api/v1/books/{book_id}/notes/{note_id}",
        headers=auth["headers"],
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Note deleted successfully"

    missing_response = client.get(
        f"/api/v1/books/{book_id}/notes/{note_id}",
        headers=auth["headers"],
    )
    assert missing_response.status_code == 404
    assert missing_response.json()["message"] == "Note not found"


def test_comments_crud_search_and_ownership_rules(client):
    owner = register_user(client, name="Owner User", email="owner@example.com")
    intruder = register_user(client, name="Intruder User", email="intruder@example.com")

    book_response = client.post(
        "/api/v1/books",
        json={"title": "Owner Book", "description": "For comments"},
        headers=owner["headers"],
    )
    book_id = book_response.json()["id"]

    note_response = client.post(
        f"/api/v1/books/{book_id}/notes",
        json={"title": "Owner Note", "content": "Original content"},
        headers=owner["headers"],
    )
    note_id = note_response.json()["id"]

    create_response = client.post(
        f"/api/v1/notes/{note_id}/comments",
        json={"content": "First comment"},
        headers=owner["headers"],
    )
    assert create_response.status_code == 201
    created_comment = create_response.json()
    comment_id = created_comment["id"]
    assert created_comment["content"] == "First comment"
    assert created_comment["user_id"] == owner["user"]["id"]

    second_comment_response = client.post(
        f"/api/v1/notes/{note_id}/comments",
        json={"content": "Searchable follow-up"},
        headers=owner["headers"],
    )
    assert second_comment_response.status_code == 201

    list_response = client.get(
        f"/api/v1/notes/{note_id}/comments?search=Searchable&author_id={owner['user']['id']}",
        headers=owner["headers"],
    )
    assert list_response.status_code == 200
    payload = list_response.json()
    assert payload["meta"]["total_items"] == 1
    assert payload["items"][0]["content"] == "Searchable follow-up"

    update_response = client.patch(
        f"/api/v1/notes/{note_id}/comments/{comment_id}",
        json={"content": "Edited comment"},
        headers=owner["headers"],
    )
    assert update_response.status_code == 200
    assert update_response.json()["content"] == "Edited comment"

    forbidden_update = client.patch(
        f"/api/v1/notes/{note_id}/comments/{comment_id}",
        json={"content": "Hacked comment"},
        headers=intruder["headers"],
    )
    assert forbidden_update.status_code == 404
    assert forbidden_update.json()["message"] == "Note not found"

    delete_response = client.delete(
        f"/api/v1/notes/{note_id}/comments/{comment_id}",
        headers=owner["headers"],
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Comment deleted successfully"

    missing_response = client.get(
        f"/api/v1/notes/{note_id}/comments/{comment_id}",
        headers=owner["headers"],
    )
    assert missing_response.status_code == 404
    assert missing_response.json()["message"] == "Comment not found"


def test_validation_errors_return_expected_shape(client):
    auth = register_user(client, name="Validation User", email="validation@example.com")

    response = client.post(
        "/api/v1/books",
        json={"title": "A", "description": "too short title"},
        headers=auth["headers"],
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["message"] == "Validation failed"
    assert payload["details"]
