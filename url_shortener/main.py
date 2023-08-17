#url_shortener/main.py
# defines the path operations

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from . import schemas
from . import crud, models
from .config import get_settings
from sqlalchemy.orm import Session
from . import models, schemas
from starlette.datastructures import URL
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine) #if the db doesn’t exist yet, then it’ll be created with all modeled tables

def get_db():               #creates and yields new database sessions with each request
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()          # closes the session once the request is finished

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)         #sets a base URL for constructing the admin URL
    admin_endpoint = app.url_path_for("admin info", secret_key=db_url.secret_key) #creates path using admin endpoint and secret key
    db_url.url = str(base_url.replace(path=db_url.key)) #creates a URL using the base URL and the URL key
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))   #creates a URL using the base URL and the admin path
    return db_url


@app.get("/")           #base path for the application
def read_root():
    return "Welcome to the URL shortener API"


@app.post("/url", response_model=schemas.URLInfo)   #accepts a URL and returns a url_key with additional info, including a secret_key
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)): #accepts a url with a DB connection
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    
    db_url = crud.create_db_url(db=db, url=url)
    #db_url.url = db_url.key               #adds key to db_url to match the required URLInfo schema that the function returns
    #db_url.admin_url = db_url.secret_key      #adds secret_key to db_url to match the required URLInfo schema
    return get_admin_info(db_url)   #returns the admin info to the user who made the request


@app.get("/{url_key}")              # accepts a URL key and forwards/redirects to your target URL
def forward_to_target_url(url_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):    #checks if a DB entry exists for the provided key
        crud.update_db_clicks(db=db, db_url=db_url) #calls click counter to increase click count
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)    #this error is raised if the DB entry does not exist


@app.get( "/admin/{secret_key}", name="admin info", response_model=schemas.URLInfo,)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):   #checks if a DB entry exists for the provided secret key
        #db_url.url = db_url.key
        #db_url.admin_url = db_url.secret_key
        return get_admin_info(db_url) #returns the admin info to the user with a valid secret key
    else:
        raise_not_found(request)


@app.delete("/admin/{secret_key}")
def delete_url(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise_not_found(request)
