def test_landing_page_renders_html(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Book &amp; Notes Management System" in response.text or "Book & Notes Management System" in response.text
    assert "Create Account" in response.text


def test_register_login_and_book_note_web_flow(client):
    register_response = client.post(
        "/register",
        data={
            "name": "Template User",
            "email": "template@example.com",
            "password": "supersecret123",
        },
        follow_redirects=True,
    )
    assert register_response.status_code == 200
    assert "Your Books" in register_response.text

    create_book_response = client.post(
        "/books",
        data={"title": "Algorithms", "description": "Interview preparation"},
        follow_redirects=True,
    )
    assert create_book_response.status_code == 200
    assert "Algorithms" in create_book_response.text

    books_page = client.get("/books")
    assert books_page.status_code == 200
    assert '/books/' in books_page.text

    import re

    book_match = re.search(r'/books/([0-9a-f\-]{36})', books_page.text)
    assert book_match
    book_id = book_match.group(1)

    note_response = client.post(
        f"/books/{book_id}/notes",
        data={"title": "Dynamic Programming", "content": "Break problems into overlapping subproblems."},
        follow_redirects=True,
    )
    assert note_response.status_code == 200
    assert "Dynamic Programming" in note_response.text

    logout_response = client.post("/logout", follow_redirects=True)
    assert logout_response.status_code == 200
    assert "Create Account" in logout_response.text


def test_login_page_shows_error_for_invalid_credentials(client):
    response = client.post(
        "/login",
        data={"email": "missing@example.com", "password": "wrongpassword"},
    )

    assert response.status_code == 400
    assert "Invalid email or password" in response.text
