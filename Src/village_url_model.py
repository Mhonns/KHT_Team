from pydantic import BaseModel

# class village_url_data(BaseModel):
#     village_name: str
#     url: str 
#     article_title: str = None 
#     posted_date: str = None

class village_url_data(BaseModel):
    village_name: str
    url: list[str] = []
    article_title: str = None 
    posted_date: str = None
    sequence: int = None



