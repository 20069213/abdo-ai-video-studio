import shutil
import uuid
from pathlib import Path
from urllib.parse import urlparse

from gradio_client import Client, handle_file


class GenerationEngine:

    def __init__(self):
        self.space_id = "OpenKing/wan2-video-generation"

        self.output_dir = (
            Path(__file__).resolve().parents[2] / "outputs"
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def is_ready(self):
        return bool(self.space_id)

    def generate_video(
        self,
        image_path=None,
        prompt="",
        duration=4
    ):
        if not prompt or not prompt.strip():
            return {
                "success": False,
                "error": "اكتب وصف الفيديو أولاً"
            }

        if not image_path:
            return {
                "success": False,
                "error": "ارفع صورة أولاً"
            }

        image_path = Path(image_path)

        if not image_path.is_file():
            return {
                "success": False,
                "error": "ملف الصورة غير موجود"
            }

        try:
            print("CONNECTING TO WAN2.2...")

            client = Client(self.space_id)

            image = handle_file(str(image_path))

            print("GENERATING VIDEO...")

            result = client.predict(
                prompt,
                image,
                1280,
                704,
                73,
                35,
                5.0,
                -1,
                api_name="/generate_video"
            )

            if not isinstance(result, (tuple, list)) or len(result) < 2:
                return {
                    "success": False,
                    "error": "استجابة غير متوقعة من محرك الفيديو"
                }

            generated_video, status = result

            if isinstance(generated_video, dict):
                source_video = generated_video.get("video")
            else:
                source_video = generated_video

            if not source_video:
                return {
                    "success": False,
                    "error": f"لم يرجع المحرك فيديو. الحالة: {status}"
                }

            source_text = str(source_video)

            if source_text.startswith(("http://", "https://")):
                from gradio_client import handle_file

                source_video = handle_file(source_text)

            source_video = Path(source_video)

            if not source_video.is_file():
                return {
                    "success": False,
                    "error": "ملف الفيديو الناتج غير موجود"
                }

            job_id = uuid.uuid4().hex
            job_dir = self.output_dir / job_id
            job_dir.mkdir(parents=True, exist_ok=True)

            destination = job_dir / "video.mp4"

            shutil.copy2(source_video, destination)

            print("VIDEO SAVED:", destination)

            return {
                "success": True,
                "message": "Video generated successfully",
                "video_path": str(destination),
                "video_url": f"/outputs/{job_id}/video.mp4",
                "status": str(status)
            }

        except Exception as error:
            print("GENERATION ERROR:", repr(error))

            return {
                "success": False,
                "error": str(error)
            }


if __name__ == "__main__":
    engine = GenerationEngine()

    print("ABDO GENERATION ENGINE READY")
    print("MODEL:", engine.space_id)
