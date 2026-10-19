
from pathlib import Path
from datetime import datetime
import json

HISTORY_FILE = (
    Path(__file__).resolve().parent.parent
    / "quiz_history.json"
)


def save_quiz_result(topic, score, total):
    percentage = (score / total) * 100 if total > 0 else 0

    result = {
        "topic": topic,
        "score": score,
        "total": total,
        "percentage": round(percentage, 1),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                history = json.load(file)
        else:
            history = []

        if not isinstance(history, list):
            history = []

        history.append(result)

        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)

        print("Quiz result saved successfully!")

    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not save quiz history: {error}")


def show_quiz_history():
    if not HISTORY_FILE.exists():
        print("\nNo quiz history yet. Complete a quiz first!")
        return

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

        if not history:
            print("\nNo quiz history yet. Complete a quiz first!")
            return

        print("\n===== QUIZ HISTORY =====")

        for number, result in enumerate(history, start=1):
            print(f"\nQuiz {number}")
            print(f"Topic: {result['topic']}")
            print(f"Score: {result['score']}/{result['total']}")
            print(f"Percentage: {result['percentage']}%")
            print(f"Date: {result['date']}")

    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"Could not read quiz history: {error}")
