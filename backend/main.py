from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.tasks import Task
from models.user import User
from routers.auth import router as auth_router
from routers.tasks import router as tasks_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/")
async def getRoot():
    return {"message": "hello"}
