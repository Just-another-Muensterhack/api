# helpwave

This is a first aid app for people in need of help.
In an emergency, this app makes it possible to inform qualified helpers in the surrounding area and thus arrive at the scene of the emergency even faster than an ambulance.

## Development
### Database Setup

Change the Directory into the root project folder and start the postgres database with docker-compose.
```bash
docker-compose up -d postgres
```

### Setup environment
Environment files: `.api.env`, `.postgres.env`

#### Console
Set the environment variables
```bash
set -a
. .api.env
. .postgres.env
set +a
```
if you are in dev mode
```bash
export POSTGRES_HOST=localhost
unset SECRET_KEY_FILE
```

#### PyCharm / Intellij

1. Open 'Edit Run/Debug configurations' dialog (on the top right)
2. Edit configuration
3. Environment variables add following string:
   `POSTGRES_HOST=localhost;POSTGRES_USER=postgres;POSTGRES_PASSWORD=S3cr3T;POSTGRES_NAME=api;POSTGRES_DB=api;POSTGRES_DB=api`
4. apply configs

### Run Project
```bash
python3 ./app/main.py
```

### Model migrations [alembic]
Change into the app directory

Running our first migration ([docs](https://alembic.sqlalchemy.org/en/latest/tutorial.html#running-our-first-migration))
```bash
alembic upgrade head
```

Auto generating migration ([docs](https://alembic.sqlalchemy.org/en/latest/autogenerate.html))
```bash
alembic revision --autogenerate -m "<your message>"
```

[MORE DOCS](https://alembic.sqlalchemy.org/en/latest/tutorial.html#running-our-first-migration)

### Linter Hacks
```bash
python -m black ./app/ --exclude --check --line-length 120
```
