import os


class PostgresConfig:
    host: str
    port: int
    db: str
    username: str
    password: str

    def __init__(self, host: str, port: int, db: str, username: str, password: str):
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password


class Config:
    configs: {str: str}

    def __init__(self):
        self.configs = dict(os.environ)

    def get_postgres_config(self) -> PostgresConfig:
        if 'POSTGRES_HOST' in tuple(self.configs.keys()):
            host = self.configs["POSTGRES_HOST"]
        else:
            host = None

        if 'POSTGRES_PORT' in self.configs.keys():
            port = self.configs["POSTGRES_PORT"]
        else:
            port = 5432

        if 'POSTGRES_DB' in self.configs.keys():
            db = self.configs["POSTGRES_DB"]
        else:
            db = None

        if 'POSTGRES_USER' in self.configs.keys():
            username = self.configs["POSTGRES_USER"]
        else:
            username = None

        if 'POSTGRES_PASSWORD' in self.configs.keys():
            password = self.configs["POSTGRES_PASSWORD"]
        else:
            password = None

        return PostgresConfig(host, port, db, username, password)
