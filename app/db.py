from sqlalchemy import create_engine

import os

from sqlalchemy.ext.declarative import declarative_base

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")


engine = create_engine(f"postgresql://{user}:{password}@{host}:5432/{database}", echo=True)

Base = declarative_base()

