
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.train_model import train
from backend.ai_model import AbdoAI


@asynccontextmanager
async def lifespan(app: FastAPI):
    train()
    app.state.ai = AbdoAI()
    yield


app = FastAPI(
    title="ABDO AI VIDEO STUDIO",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {
        "app": "ABDO AI VIDEO STUDIO",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "ABDO AI",
        "engine": "experimental_scene_classifier"
    }


@app.post("/api/analyze")
def analyze(data: PromptRequest):
    return app.state.ai.analyze(data.prompt)
