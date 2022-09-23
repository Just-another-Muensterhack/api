from sqlalchemy import create_engine

import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = os.getenv("POSTGRES_USER", "api")
password = os.getenv("POSTGRES_PASSWORD", "postgres_pw")
database = os.getenv("POSTGRES_DB", "api")
host = os.getenv("POSTGRES_HOST", "postgres")
port = os.getenv("POSTGRES_PORT", "5432")

engine = create_engine(
    f"postgresql://" f"{user}:{password}@{host}:{port}/{database}",
    echo=True,
)

Model = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
