
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "training_data.json"


def prepare_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    required_fields = ["prompt", "scene"]

    for index, item in enumerate(data):
        for field in required_fields:
            if not item.get(field):
                raise ValueError(
                    f"Missing {field} in sample {index}"
                )

    print("ABDO AI DATA PREPARATION")
    print("------------------------")
    print("Training samples:", len(data))
    print("Validation: SUCCESS")

    return data


if __name__ == "__main__":
    prepare_data()
