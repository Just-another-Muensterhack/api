from sqlalchemy import create_engine

import os

from sqlalchemy.ext.declarative import declarative_base

user = os.getenv('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
database = os.environ.get('POSTGRES_DB')


engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/{database}', echo=True)

Base = declarative_base()
