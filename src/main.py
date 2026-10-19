import json

try:
    from .gemini_helper import ask_gemini
    from .quiz_history import save_quiz_result, show_quiz_history
except ImportError:
    from gemini_helper import ask_gemini
    from quiz_history import save_quiz_result, show_quiz_history
    
def run_quiz(questions, topic):
    score = 0

    for number, question in enumerate(questions, start=1):
        print(f"\nQuestion {number}: {question['question']}")

        for option in question["options"]:
            print(option)

        answer = input("Your answer (A, B, C, or D): ").strip().lower()

        while answer not in ["a", "b", "c", "d"]:
            print("Invalid answer. Please enter A, B, C, or D.")
            answer = input("Your answer (A, B, C, or D): ").strip().lower()

        correct_letter = question["answer"]
        correct_option = ""

        for option in question["options"]:
            if option.lower().startswith(correct_letter + "."):
                correct_option = option
                break

        if answer == correct_letter:
            print("Correct!")
            score += 1
        else:
            print("Incorrect.")

        print(f"Correct answer: {correct_option}")

        explanation_prompt = f"""
You are a friendly study tutor.

Topic: {topic}
Question: {question["question"]}
Options: {question["options"]}
Correct answer: {correct_option}

Explain in simple English why the correct answer is right.
Explain briefly in 2 to 4 sentences.
Give a simple example if helpful.
"""

        print("\nAI explanation:")
        explanation = ask_gemini(explanation_prompt)
        print(explanation)

    total = len(questions)
    percentage = (score / total) * 100 if total > 0 else 0

    print("\n===== QUIZ RESULTS =====")
    print(f"Topic: {topic}")
    print(f"Your score: {score}/{total}")
    print(f"Your percentage: {percentage:.1f}%")

    if percentage == 100:
        print("Excellent! You answered every question correctly!")
    elif percentage >= 70:
        print("Great job! Keep learning!")
    elif percentage >= 50:
        print("Good effort! A little more practice will help.")
    else:
        print("Don't give up! Review the topic and try again.")

    save_quiz_result(topic, score, total)



def study_assistant():
    print("AI Study Assistant")
    print("----------------------")

    while True:
        print("\nChoose a study mode:")
        print("1. Explain a topic")
        print("2. Summarize notes")
        print("3. Generate quiz questions")
        print("4. View quiz history")
        print("5. Exit")

        choice = input("\nEnter your choice: ").strip()

        # MODE 1: Explain a topic
        if choice == "1":
            topic = input(
                "What topic do you want explained? "
            ).strip()

            if not topic:
                print("Please enter a topic.")
                continue

            print("\nGetting your explanation from AI...")

            prompt = (
                f"Explain {topic} in simple English for a beginner. "
                "Use clear sentences and give one example."
            )

            explanation = ask_gemini(prompt)

            print("\nExplanation:")
            print(explanation)

        # MODE 2: Summarize notes
        elif choice == "2":
            notes = input("Paste your notes here: ").strip()

            if not notes:
                print("Please enter some notes.")
                continue

            print("\nSummarizing your notes with AI...")

            prompt = (
                "Summarize the following study notes in simple English. "
                "Keep the most important ideas and key terms. "
                "Use bullet points where helpful.\n\n"
                f"NOTES:\n{notes}"
            )

            summary = ask_gemini(prompt)

            print("\nSummary:")
            print(summary)

        # MODE 3: Generate an AI quiz
        elif choice == "3":
            topic = input(
                "What topic should the quiz cover? "
            ).strip()

            if not topic:
                print("Please enter a topic.")
                continue

            print("\nGenerating quiz questions with AI...")

            prompt = f"""
Create exactly 5 multiple-choice quiz questions about {topic}.

Return ONLY valid JSON, with no Markdown code fences or extra text.

Use this format:
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": [
        "A. First option",
        "B. Second option",
        "C. Third option",
        "D. Fourth option"
      ],
      "answer": "a"
    }}
  ]
}}

Rules:
- Return exactly 5 questions.
- Each question must have exactly 4 options.
- Options must start with A., B., C., and D.
- The answer must be a lowercase letter: a, b, c, or d.
- The answer must match the correct option.
- Use clear English.
"""

            response = ask_gemini(prompt)

            try:
                data = json.loads(response)
                questions = data["questions"]

                if not isinstance(questions, list) or len(questions) != 5:
                    raise ValueError(
                        "The AI did not return exactly 5 questions."
                    )

                for question in questions:
                    if not isinstance(question, dict):
                        raise ValueError(
                            "A question has an invalid format."
                        )

                    if not isinstance(question.get("question"), str):
                        raise ValueError(
                            "A question is missing its text."
                        )

                    options = question.get("options")

                    if not isinstance(options, list) or len(options) != 4:
                        raise ValueError(
                            "Each question must have 4 options."
                        )

                    if question.get("answer") not in ["a", "b", "c", "d"]:
                        raise ValueError(
                            "A correct answer is missing or invalid."
                        )

                    expected_starts = ["a.", "b.", "c.", "d."]

                    for option, expected in zip(options, expected_starts):
                        if (
                            not isinstance(option, str)
                            or not option.lower().startswith(expected)
                        ):
                            raise ValueError(
                                "Options must start with A., B., C., and D."
                            )

                print(f"\nAI-generated quiz: {topic}")
                run_quiz(questions, topic)

            except (
                json.JSONDecodeError,
                KeyError,
                TypeError,
                ValueError
            ) as error:
                print("Sorry, the AI returned an invalid quiz.")
                print("Please try again.")
                print(f"Details: {error}")

        # MODE 4: View saved quiz history
        elif choice == "4":
            show_quiz_history()

        # MODE 5: Exit
        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print(
                "Invalid choice. Please choose 1, 2, 3, 4, or 5."
            )


if __name__ == "__main__":
    study_assistant()
