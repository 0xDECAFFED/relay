from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.core.database import create_db_and_tables, get_session
from app.core.encoder import encoder
from app.models.url import URL, URLCreate, URLResponse
from app.core.config import settings

# Create FastAPI app
app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.on_event("startup")
def on_startup():
    """Initialize database tables on startup."""
    create_db_and_tables()


@app.post("/", response_model=URLResponse)
def create_short_url(
    url_data: URLCreate,
    session: Session = Depends(get_session),
):
    """Create a short URL from a long URL."""
    # Check if URL already exists (optional optimization)
    existing = session.exec(
        select(URL).where(URL.original_url == url_data.url)
    ).first()

    if existing:
        return URLResponse(
            short_url=f"{settings.base_url}/{existing.short_code}",
            short_code=existing.short_code,
            original_url=existing.original_url,
        )

    # Create new URL entry
    url = URL(original_url=url_data.url, short_code="")
    session.add(url)
    session.commit()
    session.refresh(url)

    # Generate short code from ID
    short_code = encoder.encode(url.id)
    url.short_code = short_code
    session.add(url)
    session.commit()
    session.refresh(url)

    return URLResponse(
        short_url=f"{settings.base_url}/{short_code}",
        short_code=short_code,
        original_url=url.original_url,
    )


@app.get("/{short_code}")
def redirect_to_original(
    short_code: str,
    session: Session = Depends(get_session),
):
    """Redirect short code to original URL."""
    # Find URL by short code
    url = session.exec(
        select(URL).where(URL.short_code == short_code)
    ).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    # Redirect to original URL
    return RedirectResponse(url.original_url, status_code=302)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": settings.app_version}