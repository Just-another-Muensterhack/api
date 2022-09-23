import routes

from typing import Union
from fastapi import FastAPI

app = FastAPI(
    title="HelpWaveBackend",
    description="Backend which manages HelpWave users and emergencies",
    version="0.0.1",
    terms_of_service="https://api.helpwave.de",
    contact={
        "name": "USE-TO @use-to",
        "url": "https://helpwave.de",
        "email": "mail@helpwave.de",
    },
)

app.include_router(routes.users.user_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
