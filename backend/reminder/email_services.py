import os
import resend
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

resend.api_key = RESEND_API_KEY


def send_email(to, subject, body):

    params = {
        "from": "onboarding@resend.dev",
        "to": [to],
        "subject": subject,
        "text": body,
    }

    try:
        response = resend.Emails.send(params)

        return {
            "success": True,
            "message_id": response["id"]
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
        
def execute_tool(tool_name,arguments,trusted_email):
    if tool_name != "send_email":
        return 
    
    if "subject" not in arguments:
        return 
    if "body" not in arguments:
        return
    
    result = send_email(trusted_email,arguments['subject'],arguments['body'])
    return result
    