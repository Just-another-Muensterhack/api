import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from config import Config, PostgresConfig

config: Config = Config()
pg_config: PostgresConfig = config.get_postgres_config()

engine = create_engine(
    f"postgresql://{pg_config.username}:{pg_config.password}@{pg_config.host}:{pg_config.port}/{pg_config.db}",
    echo=True
)

Base = declarative_base()
