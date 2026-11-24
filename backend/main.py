from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4
from threading import Lock

from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError

from backend.train_model import train
from backend.ai_model import AbdoAI
from ai_engine.generation.engine import GenerationEngine


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

jobs = {}
jobs_lock = Lock()


@asynccontextmanager
async def lifespan(app: FastAPI):
    trained_model = train()
    app.state.ai = AbdoAI(trained_model)
    app.state.generator = GenerationEngine()
    print("ABDO AI VIDEO STUDIO READY")
    yield


app = FastAPI(
    title="ABDO AI VIDEO STUDIO",
    description="AI Video Generation Studio",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount(
    "/outputs",
    StaticFiles(directory=str(OUTPUT_DIR)),
    name="outputs"
)


def run_generation(job_id: str, image_path: str, prompt: str):
    with jobs_lock:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["message"] = "جاري إنشاء الفيديو..."

    try:
        result = app.state.generator.generate_video(
            image_path=image_path,
            prompt=prompt,
            duration=4
        )

        with jobs_lock:
            if result.get("success") and result.get("video_url"):
                jobs[job_id]["status"] = "completed"
                jobs[job_id]["video_url"] = result["video_url"]
                jobs[job_id]["message"] = "تم إنشاء الفيديو بنجاح"
            else:
                jobs[job_id]["status"] = "failed"
                jobs[job_id]["message"] = result.get(
                    "error", "فشل إنشاء الفيديو"
                )

    except Exception as error:
        with jobs_lock:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["message"] = str(error)


class PromptRequest(__import__("pydantic").BaseModel):
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
        "video_engine": "Wan2.2",
        "generation_ready": True
    }


@app.post("/api/analyze")
def analyze(data: PromptRequest):
    return app.state.ai.analyze(data.prompt)


@app.post("/api/create-video")
async def create_video(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    prompt = prompt.strip()

    if not prompt:
        raise HTTPException(
            status_code=400,
            detail="اكتب وصف الفيديو أولاً"
        )

    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="الملف المرسل ليس صورة"
        )

    image_data = await image.read()

    if not image_data:
        raise HTTPException(
            status_code=400,
            detail="الصورة فارغة"
        )

    if len(image_data) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="حجم الصورة أكبر من 10 ميجابايت"
        )

    job_id = str(uuid4())
    image_path = UPLOAD_DIR / f"{job_id}.jpg"

    try:
        import io

        with Image.open(io.BytesIO(image_data)) as img:
            img.convert("RGB").save(image_path, format="JPEG")

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="تعذر قراءة الصورة"
        )

    with jobs_lock:
        jobs[job_id] = {
            "status": "queued",
            "message": "تم استلام الطلب",
            "video_url": None
        }

    background_tasks.add_task(
        run_generation,
        job_id,
        str(image_path),
        prompt
    )

    return {
        "success": True,
        "job_id": job_id,
        "status": "queued",
        "message": "تم إرسال طلب إنشاء الفيديو"
    }


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    with jobs_lock:
        job = jobs.get(job_id)

        if not job:
            raise HTTPException(
                status_code=404,
                detail="المهمة غير موجودة"
            )

        return {
            "job_id": job_id,
            **job
        }
