from starlette.middleware.cors import CORSMiddleware

import routes

from fastapi import FastAPI

from database import Base, engine

from sqlalchemy.orm import Session
from sqlalchemy import select

from models.device import Device

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

origins = [
    "https://helpwave.de",
    "http://helpwave.de",
    "https://main.helpwave.de",
    "http://main.helpwave.de",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.user.user_router)
app.include_router(routes.emergency.emergency_router)


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:

        device1 = Device(
                    latitude=515712.9,
                    longitude=515712.2
        )

        session.add(device1)
        session.commit()

        # selected_devices = Device.query.all()
        selected_devices = session.query(Device).all()
        for device in selected_devices:
            print(device.longitude)

        session.commit()






if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
