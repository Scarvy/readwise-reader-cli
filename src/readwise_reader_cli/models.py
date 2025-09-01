from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import (
    AnyUrl,
    BaseModel,
    Field,
    HttpUrl,
    field_serializer,
    field_validator,
)


class LocationEnum(str, Enum):
    new = "new"
    later = "later"
    archive = "archive"
    feed = "feed"
    shortlist = "shortlist"


class CategoryEnum(str, Enum):
    article = "article"
    email = "email"
    rss = "rss"
    highlight = "highlight"
    note = "note"
    pdf = "pdf"
    epub = "epub"
    tweet = "tweet"
    video = "video"


class TagInfo(BaseModel):
    name: str
    type: str
    created: datetime


class ListParameters(BaseModel):
    id: Optional[str] = None
    update_after: Optional[datetime] = Field(None, serialization_alias="updatedAfter")
    category: Optional[CategoryEnum] = None
    location: Optional[LocationEnum] = None
    next_page_cursor: Optional[str] = Field(None, serialization_alias="pageCursor")


class DocumentInfo(BaseModel):
    id: Optional[str] = None
    url: HttpUrl
    title: Optional[str] = None
    author: Optional[str] = None
    source: Optional[str] = None
    category: Optional[CategoryEnum] = None
    location: Optional[LocationEnum] = None
    tags: Optional[Union[List[str], Dict[str, TagInfo]]] = None
    site_name: Optional[str] = None
    word_count: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_date: Optional[Union[date, datetime]] = None
    summary: Optional[str] = None
    image_url: Optional[Union[AnyUrl, str, None]] = None
    content: Optional[str] = None
    source_url: Optional[AnyUrl] = None
    notes: Optional[str] = None
    parent_id: Optional[str] = None
    reading_progress: Optional[float] = 0.0

    @field_validator("reading_progress")
    def validate_reading_progress(cls, value):
        if not 0.0 <= value <= 1.0:
            raise ValueError("Reading progress must be between 0 and 100")
        return value

    @field_serializer("url")
    def serialize_url(self, url: HttpUrl):
        return str(url)

    @field_serializer("published_date")
    def serialize_dt(self, dt: Union[date, datetime, None]):
        if dt:
            return dt.strftime("%Y-%m-%dT%H:%M:%S%z")
