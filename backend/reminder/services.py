from dotenv import load_dotenv
import os
import json
from groq import Groq
from .email_services import execute_tool

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")



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
                return {
                    "success": False,
                    "error": "No tool call was generated"
                }

            tool_call = message.tool_calls[0]

            tool_name = tool_call.function.name
            tool_arguments = tool_call.function.arguments
            
            data = json.loads(tool_arguments)
            result = execute_tool(tool_name,data,student_email)

            return result 
        
        except json.JSONDecodeError:

            if attempt < max_retries:
                print(
                    f"Attempt {attempt + 1} failed: "
                    f"Invalid tool arguments. Retrying..."
                )
                continue

            return {
                    "success": False,
                    "error": "Invalid tool arguments after retries"
                }

def process_pending_students(
    pending_students,
    assignment_name,
    due_date
):
    results = []
    sent = 0
    failed = 0

    for student in pending_students:

        result = generate_reminder_email(
            student["name"],
            student["email"],
            assignment_name,
            due_date
        )

        if result and result.get("success"):
            sent += 1

            results.append({
                "student": student["name"],
                "status": "sent",
                "message_id": result.get("message_id")
            })

        else:
            failed += 1

            results.append({
                "student": student["name"],
                "status": "failed",
                "error": result.get("error") if result else "Unknown error"
            })

    return {
        "total_students": len(pending_students),
        "sent": sent,
        "failed": failed,
        "results": results
    }

