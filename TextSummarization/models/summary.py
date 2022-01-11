from typing import List, Optional
from pydantic import BaseModel, Field
class Article(BaseModel):
    article: str = Field(...)
    order: Optional[ List[int] ] = None
