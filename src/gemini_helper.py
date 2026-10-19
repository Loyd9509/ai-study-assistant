
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# Load the .env file from the project folder
load_dotenv(
    Path(__file__).resolve().parent.parent / ".env",
    override=True
)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY was not found. Check your .env file."
    )

client = Groq(api_key=api_key)


def ask_gemini(prompt):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly study assistant. "
                        "Explain topics in simple English with "
                        "clear examples."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            timeout=30
        )

        answer = response.choices[0].message.content

        if not answer:
            print("The AI returned an empty response.")
            return "Sorry, the AI did not provide an answer. Please try again."

        return answer.strip()

    except Exception as error:
        print(f"\nAI request failed: {error}")
        print("Check your internet connection and try again.")

        return (
            "Sorry, I couldn't get an answer from the AI. "
            "Please try again."
        )
