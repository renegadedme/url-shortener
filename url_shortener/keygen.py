#url_shortener/keygen.py

import secrets
import string
from sqlalchemy.orm import Session
from . import crud

def create_unique_random_key(db: Session) -> str:
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):      #checks if the key already exists in the DB for a given URL
        key = create_random_key()               #generates a random key if the key exists
    return key

def create_random_key(length: int = 6) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for x in range(length))