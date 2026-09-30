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
        return {
        "success": False,
        "error": "Tool Name mismatch"
    }
    
    if "subject" not in arguments:
        return {
        "success": False,
        "error": "Subject missing"
    }
        
    if "body" not in arguments:
        return {
        "success": False,
        "error": "body Missing"
    }
    
    if not isinstance(arguments["subject"], str) or not isinstance(arguments["body"], str):
        return {
            "success":False,
            "error":"both  should be string"
        }
    
    if not arguments["subject"].strip():
        return {
                "success":False,
                "error":"it Cant be empty"
            }
    
    if not arguments["body"].strip():
        return {
           "success":False,
            "error":"it Cant be empty" 
        }
        
    result = send_email(trusted_email,arguments['subject'],arguments['body'])
    return result
    