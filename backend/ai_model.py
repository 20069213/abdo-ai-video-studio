
import joblib

from pathlib import Path

MODEL_FILE = Path(__file__).parent / "scene_model.joblib"


class AbdoAI:

    def __init__(self):
        self.model = None
        self.name = "ABDO AI"
        self.version = "1.0"

        if MODEL_FILE.exists():
            self.model = joblib.load(MODEL_FILE)

    def analyze(self, prompt):

        prompt = prompt.strip()

        if not prompt:
            return {
                "success": False,
                "error": "Prompt is empty"
            }

        if self.model is None:
            return {
                "success": False,
                "error": "Model not trained"
            }

        scene = self.model.predict([prompt])[0]

        return {
            "success": True,
            "prompt": prompt,
            "scene": scene,
            "model": self.name,
            "version": self.version
        }


ai = AbdoAI()
