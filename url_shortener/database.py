# url_shortener/database.py
# contains information about the database connection

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

engine = create_engine(
    get_settings().db_url, connect_args={"check_same_thread": False}    
)           # think of engine as the entry point to the database   
            # check_same_thread set to False allows more than 1 request at a time to the DB.          
                               
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
Base = declarative_base()           # allows us to generate a mapped Table object