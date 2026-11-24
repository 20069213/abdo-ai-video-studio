
import json
import re
from pathlib import Path
from collections import Counter, defaultdict
import math

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "training_data.json"


class SimpleAI:
    def __init__(self, data):
        self.samples = data

    def predict(self, prompts):
        results = []

        for prompt in prompts:
            words = set(re.findall(r"\w+", prompt.lower()))
            scores = defaultdict(float)

            for item in self.samples:
                sample_words = set(
                    re.findall(r"\w+", item["prompt"].lower())
                )

                common = words & sample_words
                if common:
                    scores[item["scene"]] += len(common) / math.sqrt(
                        len(sample_words)
                    )

            if scores:
                results.append(max(scores, key=scores.get))
            else:
                results.append("unknown")

        return results


def train():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    model = SimpleAI(data)

    print("ABDO AI TRAINING COMPLETE")
    print("Training samples:", len(data))

    return model

