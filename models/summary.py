from typing import List, Optional
from pydantic import BaseModel, Field
class Article(BaseModel):
    article: dict = Field(...)
    #t_clusters: int = Field(...) 
    fpath: str = Field(...)
    order: Optional[ dict ] = None

class Vidpath(BaseModel):
    path: str = Field(...)
    #v_clusters: int = Field(...) 
    order: Optional[ List[int] ] = None
    fr: Optional[int] = None
    t_chunks: Optional[int] = None
