
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ABDO AI VIDEO STUDIO",
    description="AI Video Generation Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "app": "ABDO AI VIDEO STUDIO",
        "status": "online",
        "message": "Welcome to ABDO AI"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "python": True,
        "video_engine": "not_connected"
    }

@app.get("/api/features")
def features():
    return {
        "text_to_video": True,
        "image_to_video": True,
        "ai_voice": True,
        "subtitles": True,
        "video_export": True
    }
