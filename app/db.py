from sqlalchemy import create_engine

import os

from sqlalchemy.ext.declarative import declarative_base

User = os.getenv('POSTGRES_USER')
Password = os.environ.get('POSTGRES_PASSWORD')
Database = os.environ.get('POSTGRES_DB')

print(User, Password, Database)

engine = create_engine(f'postgresql://{User}:{Password}@localhost:5432/{Database}', echo=True)

Base = declarative_base()


