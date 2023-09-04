from datetime import date, datetime
from enum import Enum
from typing import Dict, Optional, List, Union

from pydantic import BaseModel, HttpUrl, AnyUrl, field_validator, field_serializer


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
        if not 0 <= value <= 100:
            raise ValueError("Reading progress must be between 0 and 100")
        return value

    @field_serializer("url")
    def serialize_url(self, url: HttpUrl):
        return str(url)

    @field_serializer("published_date")
    def serialize_dt(self, dt: Union[date, datetime, None]):
        if dt:
            return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


if __name__ == "__main__":
    sample_document = {
        "id": "01h8707jqgjsfzznh281xxashb",
        "url": "https://read.readwise.io/read/01h8707jqgjsfzznh281xxashb",
        "title": "Large language models, explained with a minimum of math and jargon",
        "author": "Timothy B Lee",
        "source": None,
        "category": "article",
        "location": "new",
        "tags": {
            "shortlist": {
                "name": "shortlist",
                "type": "manual",
                "created": 1692640034398,
            },
        },
        "site_name": "understandingai.org",
        "word_count": 6117,
        "created_at": "2023-08-19T13:37:24.567027+00:00",
        "updated_at": "2023-08-21T18:34:24.731100+00:00",
        "published_date": 1690416000000,
        "summary": "Want to really understand how large language models work? Here’s a gentle primer.",
        "image_url": "https://substackcdn.com/image/fetch/w_1200,h_600,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc3e159bd-1228-4205-b1eb-5898ab9172d3_1600x856.png",
        "content": None,
        "source_url": "https://link.sbstck.com/redirect/08f86d22-19a6-4cc1-b449-0eebe03603dd?j=eyJ1IjoiY2gzcTgifQ.mfKJkm1MFmHg0LGeKdRGUAyRwWsVKwDUCVREGN0XyUw",
        "notes": "A model so vast,\nWords flow like a river wide,\nIntelligence reigns.",
        "parent_id": None,
        "reading_progress": 0.035575772085228635,
    }

    sample_highlight = {
        "id": "01h7mzsdxnr5jhkk9phq4e7r6f",
        "url": "https://read.readwise.io/read/01h7mzsdxnr5jhkk9phq4e7r6f",
        "title": None,
        "author": None,
        "source": "reader-mobile-app",
        "category": "highlight",
        "location": None,
        "tags": {},
        "site_name": None,
        "word_count": None,
        "created_at": "2023-08-12T13:43:21.391437+00:00",
        "updated_at": "2023-08-12T13:43:28.966254+00:00",
        "published_date": None,
        "summary": None,
        "image_url": None,
        "content": "pragmatism",
        "source_url": None,
        "notes": "",
        "parent_id": "01h7mqyeq11jt98epzcfbpde9e",
        "reading_progress": 0,
    }

    sample_note = {
        "id": "01h8m0et3vf7f3a0c7nbmhkxjg",
        "url": "https://read.readwise.io/read/01h8m0et3vf7f3a0c7nbmhkxjg",
        "title": None,
        "author": None,
        "source": "reader-web-app",
        "category": "note",
        "location": "later",
        "tags": None,
        "site_name": None,
        "word_count": 0,
        "created_at": "2023-08-24T14:51:29.042109+00:00",
        "updated_at": "2023-08-24T14:51:29.042125+00:00",
        "published_date": None,
        "summary": None,
        "image_url": None,
        "content": "Begets: 'Begets' is a verb that means to cause or bring about something. It is often used in the context of a negative cycle or pattern that perpetuates itself, such as 'violence begets violence' or 'ignorance begets ignorance.' In programming, the phrase 'bad code begets bad code' suggests that poorly written code can lead to more poorly written code, creating a cycle of inefficiency and difficulty in maintaining the program.",
        "source_url": None,
        "notes": "",
        "parent_id": "01h8m0eks760p1bj583wf9jcas",
        "reading_progress": 0,
    }

    document_info = DocumentInfo(**sample_document)
    document_info_highlight = DocumentInfo(**sample_highlight)
    document_info_note = DocumentInfo(**sample_note)
