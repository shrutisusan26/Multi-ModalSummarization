from typing import List, Optional
from pydantic import BaseModel, Field
class Article(BaseModel):
    """ A
    A data model for instantiating input passed to the /summary API.

    Attributes:
        article : dict
            A dictionary of timestamps and corresponding transcript sentences.
        t_clusters : int
            Number of text clusters used for generating optimum number of sentences.
            in the summary
        fpath : str
            Path to file.
        order : dict
            Stores a dictionay containing summary sentences.
    """      
    article: dict = Field(...)
    t_clusters: int = Field(...) 
    fpath: str = Field(...)
    order: Optional[ dict ] = None

class Vidpath(BaseModel):
    """ 
    A data model for instantiating input passed to the /vsummary API.

    Attributes:
        path : str
            Path to file.
        v_clusters : int
            Number of video clusters used for generating optimum number of key-frames.
        order: list
            Stores a list of integers corresponding to frame numbers.
        fr : int
            Frame rate used to parse the video.
        t_chunks : int
            Number of chunks of size 16 in the entire video.
    """    
    path: str = Field(...)
    v_clusters: int = Field(...) 
    order: Optional[ List[int] ] = None
    fr: Optional[int] = None
    t_chunks: Optional[int] = None
    
class Transcript(BaseModel):
    """ 
    A data model for instantiating input passed to the /link API.

    Attributes:
        url : str
            URL to video to be uploaded.
    """
    url: str = Field(...)
    
