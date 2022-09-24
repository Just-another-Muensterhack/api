from starlette.middleware.cors import CORSMiddleware

import routes

from fastapi import FastAPI

from database import Base, engine

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import func


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

        device1 = Device(latitude=51.961563, longitude=7.628202, geo=func.ST_Point(51.961563, 7.628202))
        device2 = Device(latitude=52.283333, longitude=8.050000, geo=func.ST_Point(52.283333, 8.050000))

        session.add(device1)
        session.add(device2)

        session.commit()

        # selected_devices = session.query(Device).all()
        # for device in selected_devices:
        #     print(device.longitude)

        # devices = Device()
        selected_devices_radius = device1.get_devices_within_radius(radius=99999999999999999999999999999999)
        for device in selected_devices_radius:
            # distance = session.query(func.ST_DistanceSphere(device.geo, device1.geo)).one()[0]
            print(len(device))
        # print(distance)

        distance = func.ST_DistanceSphere(device1.geo, device2.geo)
        print(distance)

        session.commit()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
