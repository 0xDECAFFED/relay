import pytest
from fastapi.testclient import TestClient

from main import app
from app.core.config import settings
from sqlmodel import SQLModel, Session, create_engine, select
from app.models.url import URL

# Create a test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, echo=False)


@pytest.fixture(scope="module")
def test_db():
    """Create test database tables."""
    SQLModel.metadata.create_all(engine)
    yield
    # Cleanup
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def db_session(test_db):
    """Create a test database session."""
    with Session(engine) as session:
        yield session


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestCreateShortURL:
    """Test cases for creating short URLs."""

    def test_create_short_url_success(self, client):
        """Test successful URL shortening."""
        response = client.post("/", json={"url": "https://example.com"})
        assert response.status_code == 200
        data = response.json()
        assert "short_url" in data
        assert "short_code" in data
        assert "original_url" in data
        assert data["original_url"] == "https://example.com"

    def test_create_short_url_invalid_format(self, client):
        """Test URL shortening with invalid URL format."""
        response = client.post("/", json={"url": "not-a-valid-url"})
        # Should fail validation
        assert response.status_code == 422

    def test_create_short_url_empty_body(self, client):
        """Test URL shortening with empty body."""
        response = client.post("/", json={})
        assert response.status_code == 422


class TestRedirectToOriginal:
    """Test cases for redirecting to original URLs."""

    def test_redirect_success(self, client, db_session):
        """Test successful redirect."""
        # Create a URL in the database
        url = URL(original_url="https://example.com", short_code="test123")
        db_session.add(url)
        db_session.commit()

        # Test redirect
        response = client.get("/test123", follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["location"] == "https://example.com"

    def test_redirect_not_found(self, client):
        """Test redirect with non-existent short code."""
        response = client.get("/nonexistent", follow_redirects=False)
        assert response.status_code == 404

    def test_redirect_empty_code(self, client):
        """Test redirect with empty short code."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 405  # Method not allowed (GET vs POST)


class TestHealthCheck:
    """Test cases for health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data