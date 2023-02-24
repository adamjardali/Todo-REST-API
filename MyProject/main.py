from fastapi import FastAPI 
from config.database import engine
import config.models
from routers import User, Auth, Task
app = FastAPI()

config.models.Base.metadata.create_all(engine)

app.include_router(User.router)
app.include_router(Auth.router)
app.include_router(Task.router)
