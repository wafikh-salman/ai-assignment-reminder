from dotenv import load_dotenv
import os
import json
from groq import Groq
from email_services import execute_tool

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


def generate_reminder_email(studentname,student_email,assignment_name, due_date):

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
    - Generate the reminder email and use the send_email tool.
    - Do not generate or modify the recipient email address.
    - The backend controls the recipient.
    - Do not add markdown.
"""
    email_tool = [
        {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "Send an assignment reminder email to a student.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "Subject of the reminder email"
                        },
                        "body": {
                            "type": "string",
                            "description": "Body of the reminder email"
                        }
                    },
                    "required": ["subject", "body"]
                }
            }
        }
]
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
            model="openai/gpt-oss-20b",
            tools=email_tool,
            tool_choice="required"
        )
        try:
            
            message = response.choices[0].message

            if not message.tool_calls:
                print("No tool call was generated")
                return None

            tool_call = message.tool_calls[0]

            tool_name = tool_call.function.name
            tool_arguments = tool_call.function.arguments
            
            data = json.loads(tool_arguments)
            result = execute_tool(tool_name,data,student_email)

            return result 
        
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

def process_pending_students(
    pending_students,
    assignment_name,
    due_date
):
    results = []

    for student in pending_students:

        result = generate_reminder_email(
            student["name"],
            student["email"],
            assignment_name,
            due_date
        )

        results.append({
            "student": student["name"],
            "result": result
        })

    return results


result = generate_reminder_email(
    "Rahul",
    "wafikhsalman07@gmail.com",
    "Python Assignment 3",
    "2026-09-30"
)

print(result)