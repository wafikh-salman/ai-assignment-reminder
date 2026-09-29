from dotenv import load_dotenv
import os
import json
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def validate_reminder_email(
    generated_data,
    student_name,
    assignment_name,
    due_date
):
    if "subject" not in generated_data:
        return False, "missing subject"

    if "body" not in generated_data:
        return False, "missing body"

    if student_name not in generated_data["body"]:
        return False, "missing student name"

    if assignment_name not in generated_data["body"]:
        return False, "missing assignment name"

    if due_date not in generated_data["body"]:
        return False, "missing due date"

    return True, None


def generate_reminder_email(studentname, assignment_name, due_date):

    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""
Role:
    You are an academic assignment reminder assistant.

Task:
    Generate a short reminder email using only the provided information.

Information:
    Student name: {studentname}
    Assignment: {assignment_name}
    Due date: {due_date}

Instructions:
    - Do not add information that was not provided.
    - Keep the email minimal and professional.
    - Do not invent deadlines, penalties, marks, or other details.

Output:
    Return only valid JSON:

    {{
        "subject": "...",
        "body": "..."
    }}

    - Do not add markdown.
    - Do not add any fields other than "subject" and "body".
"""

    max_retries = 2

    for attempt in range(max_retries + 1):

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="openai/gpt-oss-20b"
        )

        raw_data = response.choices[0].message.content

        try:
            data = json.loads(raw_data)

        except json.JSONDecodeError:
            reason = "invalid JSON response"

            if attempt < max_retries:
                print(
                    f"Attempt {attempt + 1} failed: {reason}. "
                    f"Retrying..."
                )
                continue

            print(
                f"All attempts failed. "
                f"Last reason: {reason}"
            )
            return None


        is_valid, reason = validate_reminder_email(
            data,
            studentname,
            assignment_name,
            due_date
        )

        if is_valid:
            print(f"Valid response on attempt {attempt + 1}")
            return data


        if attempt < max_retries:

            prompt = f"""
        The previous generated email failed validation.

        Validation failure:
        {reason}

        Generate the email again.

        Information:
        Student name: {studentname}
        Assignment: {assignment_name}
        Due date: {due_date}

        Requirements:
        - Use only the provided information.
        - Correct the validation problem.
        - Keep the email minimal and professional.
        - Do not invent deadlines, penalties, marks, or other details.
        - Return only valid JSON.
        - Use exactly these fields:

        {{
            "subject": "...",
            "body": "..."
        }}
        """

            print(
                f"Attempt {attempt + 1} failed: {reason}. "
                f"Retrying..."
            )

        else:
            print(
                f"All attempts failed. "
                f"Last reason: {reason}"
            )
            return None


result = generate_reminder_email(
    "Rahul",
    "Python Assignment 3",
    "2026-09-30"
)

print(result)