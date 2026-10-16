from fastapi import FastAPI
from Backend.database.database import engine
from Backend.database.models import Base
from Backend.routes.taskroutes import router as taskroutes



## Initialistion of app
app = FastAPI()

## initialisation of DB
Base.metadata.create_all(bind=engine)

app.include_router(taskroutes)