from .router import router as organization_router
from .database import create_tables, new_session
from contextlib import asynccontextmanager
from fastapi import FastAPI
from . import test_data
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await test_data.load(new_session())
    print("База готова")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)

app.include_router(organization_router)


def run() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)
