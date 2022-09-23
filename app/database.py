import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT", "5432")

engine = create_engine(
    f"postgresql://"
    f"{user}:{password}@{host}:{port}"
    f"/{database}",
    echo=True)

Model = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
