from fastapi import FastAPI

from db import engine
from models import Base
from routers import router

app = FastAPI()


@app.on_event("startup")
def startup():
    app.include_router(router)
    Base.metadata.create_all(engine)
