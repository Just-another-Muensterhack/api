from typing import Union

from fastapi import FastAPI

from database import Model, engine
from schema.user import User

app = FastAPI()

# create database schema
Model.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
