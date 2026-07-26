from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import initialize_database
from .routers import blog, looks


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="API Versalhes",
    description="Backend dos objetos e mensagens do blog.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blog.router, prefix="/api")
app.include_router(looks.router, prefix="/api")


@app.get("/api/saude", tags=["sistema"])
def verificar_saude():
    return {"status": "ok"}


# Mantém frontend e API no mesmo domínio, tanto localmente quanto no Render.
FRONTEND_DIR = Path(__file__).resolve().parents[2]
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
