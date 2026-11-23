
class AbdoAI:

    def __init__(self, trained_model):
        self.model = trained_model
        self.name = "ABDO AI"
        self.version = "1.0"

    def analyze(self, prompt):

        prompt = prompt.strip()

        if not prompt:
            return {
                "success": False,
                "error": "Prompt is empty"
            }

        scene = self.model.predict([prompt])[0]

        return {
            "success": True,
            "prompt": prompt,
            "scene": scene,
            "model": self.name,
            "version": self.version
        }
