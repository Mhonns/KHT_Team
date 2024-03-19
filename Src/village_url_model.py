from pydantic import BaseModel

class village_url_data(BaseModel):
    village_name: str
    url: str
    article_title: str
    posted_date: str