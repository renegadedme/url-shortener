# url_shortener/schemas.py
# defines the types for input/output validation

from pydantic import BaseModel

class URLBase(BaseModel):
    target_url: str

class URL(URLBase):
    is_active: bool
    clicks: int

    class Config:                   # this class lets pydantic interact with the DB model
        orm_mode = True

class URLInfo(URL):
    url: str
    admin_url: str