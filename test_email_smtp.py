#!/usr/bin/env python3

import sys
from datetime import datetime
from send_email_smtp import send_email_smtp
from config import FROM_EMAIL, TO_EMAIL, EMAIL_PASSWORD, get_email_subject, get_email_body

def test_smtp_email():
    """Test SMTP email functionality"""
    
    print("🧪 Testing SMTP Email System (No Token Expiry!)")
    print("=" * 50)
    
    # Check if email password is configured
    if EMAIL_PASSWORD == 'your-email-app-password-here':
        print("❌ Email password not configured!")
        print("   Please set EMAIL_PASSWORD in config.py or environment variable")
        print("   For Gmail: Generate an 'App Password' (not your regular password)")
        return False
    
    print(f"📧 From: {FROM_EMAIL}")
    print(f"📧 To: {TO_EMAIL}")
    print(f"🔑 Password configured: {'*' * len(EMAIL_PASSWORD[:4])}...")
    
    # Test email content
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    test_filename = f"gitlab_activity_report_{current_date}.csv"
    
    subject = f"[TEST SMTP] {get_email_subject(current_date)}"
    body = f"This is a test email using SMTP (works forever!).\n\n{get_email_body(current_date, current_timestamp, test_filename)}"
    
    print(f"📧 Subject: {subject}")
    print("-" * 50)
    
    # Send test email
    print("🚀 Sending test email via SMTP...")
    
    success = send_email_smtp(
        from_email=FROM_EMAIL,
        password=EMAIL_PASSWORD,
        to_email=TO_EMAIL,
        subject=subject,
        body=body
    )
    
    return success

def main():
    """Main test function"""
    
    print("Starting SMTP email test...\n")
    
    success = test_smtp_email()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SMTP Email test PASSED! Ready for daily automation.")
        print("💡 This email method works forever (no token expiry)")
        return 0
    else:
        print("❌ SMTP Email test FAILED. Check configuration.")
        print("\n💡 Setup instructions:")
        print("   1. For Gmail: Enable 2FA and generate App Password")
        print("   2. Go to Google Account → Security → App passwords")
        print("   3. Generate password for 'Mail' application")
        print("   4. Use that 16-character password (not your regular password)")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 