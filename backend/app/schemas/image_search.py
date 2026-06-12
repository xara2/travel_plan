from pydantic import BaseModel


class ImageSearchRequest(BaseModel):
    query: str
    destination: str = ""
    category: str = ""
    count: int = 5


class ImageResult(BaseModel):
    url: str
    alt_text: str
    thumbnail_url: str = ""
    source: str = ""
