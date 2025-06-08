#!/usr/bin/env python3

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import sys
from datetime import datetime
from config import FROM_EMAIL, TO_EMAIL

def send_email_smtp(from_email, password, to_email, subject, body, attachment_path=None):
    """
    Send email using SMTP (Gmail, Outlook, etc.)
    
    Args:
        from_email (str): Sender email address
        password (str): Email password or app password
        to_email (str): Recipient email address
        subject (str): Email subject
        body (str): Email body text
        attachment_path (str): Path to attachment file (optional)
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            try:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}',
                )
                msg.attach(part)
                print(f"📎 Attachment added: {os.path.basename(attachment_path)}")
                
            except Exception as e:
                print(f"❌ Error adding attachment: {str(e)}")
                return False
        
        # Determine SMTP server based on email domain
        email_domain = from_email.split('@')[1].lower()
        
        if 'gmail' in email_domain:
            smtp_server = "smtp.gmail.com"
            port = 587
        elif 'outlook' in email_domain or 'hotmail' in email_domain or 'live' in email_domain:
            smtp_server = "smtp-mail.outlook.com"
            port = 587
        elif 'yahoo' in email_domain:
            smtp_server = "smtp.mail.yahoo.com"
            port = 587
        elif 'simplyfi.tech' in email_domain:
            # Custom domain - you may need to check with your email provider
            smtp_server = "smtp.gmail.com"  # If using Google Workspace
            port = 587
        else:
            print(f"❌ Unknown email provider for {email_domain}")
            print("   Please configure SMTP settings manually in the script")
            return False
        
        print(f"📧 Using SMTP server: {smtp_server}:{port}")
        
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Enable TLS encryption
        server.login(from_email, password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        
        print("✅ Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        print("\n💡 Common issues:")
        print("   - For Gmail: Use 'App Password' instead of regular password")
        print("   - Enable 2-factor authentication and generate app password")
        print("   - Check if 'Less secure app access' is enabled (not recommended)")
        return False

def main():
    """Main function for command line usage"""
    
    if len(sys.argv) < 5:
        print("Usage: python3 send_email_smtp.py <from_email> <password> <to_email> <subject> <body> [attachment]")
        print("Example: python3 send_email_smtp.py sender@gmail.com app_password recipient@domain.com 'Subject' 'Body' report.csv")
        sys.exit(1)
    
    from_email = sys.argv[1]
    password = sys.argv[2]
    to_email = sys.argv[3]
    subject = sys.argv[4]
    body = sys.argv[5]
    attachment_path = sys.argv[6] if len(sys.argv) > 6 else None
    
    success = send_email_smtp(from_email, password, to_email, subject, body, attachment_path)
    
    if success:
        print(f"📧 Email sent to {to_email} at {datetime.now()}")
        sys.exit(0)
    else:
        print(f"❌ Failed to send email to {to_email}")
        sys.exit(1)

if __name__ == "__main__":
    main() 