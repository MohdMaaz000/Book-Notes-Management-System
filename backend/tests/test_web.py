def test_landing_page_renders_html(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Book &amp; Notes Management System" in response.text or "Book & Notes Management System" in response.text
    assert "Create Account" in response.text


def test_static_stylesheet_is_served(client):
    response = client.get("/static/styles.css")

    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]
    assert ".page-shell" in response.text


def test_favicon_and_robots_are_served(client):
    favicon_response = client.get("/favicon.ico")
    robots_response = client.get("/robots.txt")

    assert favicon_response.status_code == 200
    assert "image/svg+xml" in favicon_response.headers["content-type"]
    assert robots_response.status_code == 200
    assert "Allow: /" in robots_response.text


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
    assert "Account created successfully." in register_response.text
    assert "Your Books" in register_response.text

    create_book_response = client.post(
        "/books",
        data={"title": "Algorithms", "description": "Interview preparation"},
        follow_redirects=True,
    )
    assert create_book_response.status_code == 200
    assert "Book created successfully." in create_book_response.text
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
    assert "Note added successfully." in note_response.text
    assert "Dynamic Programming" in note_response.text

    logout_response = client.post("/logout", follow_redirects=True)
    assert logout_response.status_code == 200
    assert "You have been logged out." in logout_response.text
    assert "Create Account" in logout_response.text


def test_login_page_shows_error_for_invalid_credentials(client):
    response = client.post(
        "/login",
        data={"email": "missing@example.com", "password": "wrongpassword"},
    )

    assert response.status_code == 400
    assert "Invalid email or password" in response.text


def test_register_page_shows_validation_error_for_short_name(client):
    response = client.post(
        "/register",
        data={
            "name": "A",
            "email": "template@example.com",
            "password": "supersecret123",
        },
    )

    assert response.status_code == 400
    assert "Name: String should have at least 2 characters" in response.text


def test_register_page_shows_validation_error_for_short_password(client):
    response = client.post(
        "/register",
        data={
            "name": "Template User",
            "email": "template@example.com",
            "password": "123456",
        },
    )

    assert response.status_code == 400
    assert "Password: String should have at least 8 characters" in response.text
