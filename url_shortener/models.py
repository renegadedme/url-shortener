# url_shortener/models.py
# describes the content/structure of the database

from sqlalchemy import Boolean, Column, Integer, String
from .database import Base          # imports Base from database.py, allowing creation of a Table object

class URL(Base):                    # creates a database model called URL, a subclass of Base
    __tablename__ = "urls"          # defines a table called 'urls'

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True) #key contains the random string that will be part of the shortened URL
    secret_key = Column(String, unique=True, index=True) #secret key helps a user manage their shortened URL and see statistics
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)