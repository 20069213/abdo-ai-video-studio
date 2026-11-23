
import json
import joblib

from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).parent

DATA_FILE = BASE_DIR / "training_data.json"
MODEL_FILE = BASE_DIR / "scene_model.joblib"


def train():

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    prompts = [item["prompt"] for item in data]
    labels = [item["scene"] for item in data]

    model = Pipeline([
        ("vectorizer", CountVectorizer()),
        ("classifier", MultinomialNB())
    ])

    model.fit(prompts, labels)

    joblib.dump(model, MODEL_FILE)

    print("ABDO AI TRAINING COMPLETE")
    print("Training samples:", len(data))

    return model
