from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class URL(SQLModel, table=True):
    """URL model for storing shortened links."""

    id: Optional[int] = Field(default=None, primary_key=True)
    original_url: str = Field(max_length=2048)
    short_code: str = Field(max_length=255, unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class URLCreate(SQLModel):
    """Schema for creating a new URL."""

    url: str


class URLResponse(SQLModel):
    """Schema for URL response."""

    short_url: str
    short_code: str
    original_url: str