#!/usr/bin/env python3

import requests
import json
import base64
import os
import sys
from datetime import datetime
from config import GRAPH_TOKEN, FROM_EMAIL, TO_EMAIL

def send_email_with_graph(token, recipient, subject, body, attachment_path=None):
    """
    Send email using Microsoft Graph API
    
    Args:
        token (str): Microsoft Graph access token
        recipient (str): Email address of the recipient
        subject (str): Email subject
        body (str): Email body text
        attachment_path (str): Path to attachment file (optional)
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    # Graph API endpoint for sending emails
    url = "https://graph.microsoft.com/v1.0/me/sendMail"
    
    # Headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Email data structure
    email_data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient
                    }
                }
            ]
        }
    }
    
    # Add attachment if provided
    if attachment_path and os.path.exists(attachment_path):
        try:
            with open(attachment_path, 'rb') as file:
                file_content = file.read()
                file_name = os.path.basename(attachment_path)
                
                # Encode file content to base64
                file_base64 = base64.b64encode(file_content).decode('utf-8')
                
                # Add attachment to email
                email_data["message"]["attachments"] = [
                    {
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "name": file_name,
                        "contentType": "text/csv",
                        "contentBytes": file_base64
                    }
                ]
                
                print(f"Attachment added: {file_name} ({len(file_content)} bytes)")
                
        except Exception as e:
            print(f"Error processing attachment: {str(e)}")
            return False
    
    try:
        # Send the email
        response = requests.post(url, headers=headers, json=email_data)
        
        if response.status_code == 202:
            print("Email sent successfully!")
            return True
        else:
            print(f"Failed to send email. Status code: {response.status_code}")
            
            # Parse error response for better debugging
            try:
                error_data = response.json()
                error_code = error_data.get('error', {}).get('code', 'Unknown')
                error_message = error_data.get('error', {}).get('message', 'Unknown error')
                
                print(f"Error Code: {error_code}")
                print(f"Error Message: {error_message}")
                
                # Provide specific guidance based on error type
                if error_code == "InvalidAuthenticationToken":
                    print("\n🚨 Token Issue:")
                    print("   - Your token may be expired (tokens usually last 1 hour)")
                    print("   - Get a fresh token from Microsoft Graph Explorer")
                    print("   - Ensure the token has 'Mail.Send' permission")
                elif error_code == "Forbidden" or "insufficient" in error_message.lower():
                    print("\n🚨 Permissions Issue:")
                    print("   - Your token lacks 'Mail.Send' permission")
                    print("   - Go to Graph Explorer and add Mail.Send scope")
                    print("   - Consent to the permission and get a new token")
                else:
                    print(f"\n🚨 Unexpected Error: {error_code}")
                    
            except:
                print(f"Raw Response: {response.text}")
                
            return False
            
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def main():
    """Main function to handle command line arguments"""
    
    if len(sys.argv) < 4:
        print("Usage: python3 send_email_graph.py <recipient> <subject> <body> [attachment_path]")
        print("Example: python3 send_email_graph.py 'user@domain.com' 'Subject' 'Email body' '/path/to/file.csv'")
        sys.exit(1)
    
    recipient = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachment_path = sys.argv[4] if len(sys.argv) > 4 else None
    
    # Use token and email from config
    token = GRAPH_TOKEN
    
    # Send the email
    success = send_email_with_graph(token, recipient, subject, body, attachment_path)
    
    if success:
        print(f"Email sent to {recipient} at {datetime.now()}")
        sys.exit(0)
    else:
        print(f"Failed to send email to {recipient}")
        sys.exit(1)

if __name__ == "__main__":
    main() 