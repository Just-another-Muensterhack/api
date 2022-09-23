from starlette.middleware.cors import CORSMiddleware

import routes
import uuid
from datetime import datetime

from fastapi import FastAPI

from database import Model, engine
from schema.user import User
from schema.registered_user import RegisteredUser


app = FastAPI(
    title="helpwave-backend",
    description="Backend which manages helpwave users and emergencies",
    version="0.0.1",
    terms_of_service="https://api.helpwave.de",
    contact={
        "name": "helpwave",
        "url": "https://helpwave.de",
        "email": "mail@helpwave.de",
    },
)

origins = ["https://helpwave.de", "http://helpwave.de", "https://main.helpwave.de", "http://main.helpwave.de", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.user.user_router)
app.include_router(routes.emergency.emergency_router)

Model.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
