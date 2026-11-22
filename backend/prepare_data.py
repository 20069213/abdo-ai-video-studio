
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "training_data.json"

def prepare_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    required = ["prompt", "scene"]

    for index, item in enumerate(data):
        for field in required:
            if not item.get(field):
                raise ValueError(
                    f"Invalid sample: {index}, field: {field}"
                )

    print("ABDO AI DATA")
    print("Samples:", len(data))
    print("Validation: SUCCESS")

    return data


if __name__ == "__main__":
    prepare_data()
