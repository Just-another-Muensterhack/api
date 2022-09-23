from sqlalchemy import create_engine

import os

from sqlalchemy.ext.declarative import declarative_base

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT", "5432")

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}", echo=True)

Base = declarative_base()
