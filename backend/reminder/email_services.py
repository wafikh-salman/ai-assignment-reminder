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
            "message_id": response["id"],
            "retryable": False
        }

    except Exception as e:
        error_message = str(e)
        if "Invalid `to` field" in error_message:
            return {
            "success": False,
            "error": error_message,
            "retryable": False
        }
        
        return {
            "success": False,
            "error": error_message,
            "retryable": True
        }
        
def execute_tool(tool_name,arguments,trusted_email):
    if tool_name != "send_email":
        return {
        "success": False,
        "error": "Tool Name mismatch",
        "retryable": True
    }
    
    if "subject" not in arguments:
        return {
        "success": False,
        "error": "Subject missing",
        "retryable": True
    }
        
    if "body" not in arguments:
        return {
        "success": False,
        "error": "body Missing",
        "retryable": True
    }
    
    if not isinstance(arguments["subject"], str) or not isinstance(arguments["body"], str):
        return {
            "success":False,
            "error":"both  should be string",
            "retryable": True
        }
    
    if not arguments["subject"].strip():
        return {
                "success":False,
                "error":"it Cant be empty",
                "retryable": True
            }
    
    if not arguments["body"].strip():
        return {
           "success":False,
            "error":"it Cant be empty" ,
            "retryable": True
        }
        
    result = send_email(trusted_email,arguments['subject'],arguments['body'])
    return result
    