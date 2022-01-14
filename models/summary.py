from typing import List, Optional
from pydantic import BaseModel, Field
class Article(BaseModel):
    article: dict = Field(...)
    order: Optional[ dict ] = None

class Vidpath(BaseModel):
    path: str = Field(...)
    order: Optional[ List[int] ] = None
    fr: Optional[int] = None
