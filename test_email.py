#!/usr/bin/env python3

import sys
from datetime import datetime
from send_email_graph import send_email_with_graph
from config import GRAPH_TOKEN, FROM_EMAIL, TO_EMAIL, get_email_subject, get_email_body

def test_email_functionality():
    """Test the email functionality with or without attachment"""
    
    print("🧪 Testing GitLab Monitoring Email System")
    print("=" * 50)
    
    # Test email content
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    test_filename = f"gitlab_activity_report_{current_date}.csv"
    
    subject = get_email_subject(current_date)
    body = get_email_body(current_date, current_timestamp, test_filename)
    
    print(f"📧 From: {FROM_EMAIL}")
    print(f"📧 To: {TO_EMAIL}")
    print(f"📧 Subject: {subject}")
    print(f"📧 Body Preview:")
    print(body[:200] + "..." if len(body) > 200 else body)
    print("-" * 50)
    
    # Check if we have a token
    if GRAPH_TOKEN == 'your-graph-token-here':
        print("❌ Error: Microsoft Graph token not configured!")
        print("   Please update config.py with your actual Graph token")
        return False
    
    print("🔑 Graph token configured ✓")
    
    # Test email without attachment first
    print("\n🚀 Sending test email (without attachment)...")
    
    success = send_email_with_graph(
        token=GRAPH_TOKEN,
        recipient=TO_EMAIL,
        subject=f"[TEST] {subject}",
        body=f"This is a test email.\n\n{body}"
    )
    
    if success:
        print("✅ Test email sent successfully!")
        return True
    else:
        print("❌ Test email failed!")
        return False

def test_email_with_attachment():
    """Test email with an actual CSV attachment if it exists"""
    
    import os
    import glob
    
    # Look for existing CSV reports
    csv_files = glob.glob("gitlab_activity_report_*.csv")
    
    if not csv_files:
        print("ℹ️  No CSV reports found to test attachment functionality")
        return True
    
    # Use the most recent CSV file
    latest_csv = max(csv_files, key=os.path.getctime)
    
    print(f"\n📎 Testing email with attachment: {latest_csv}")
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    subject = f"[TEST WITH ATTACHMENT] {get_email_subject(current_date)}"
    body = f"This is a test email with attachment.\n\n{get_email_body(current_date, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), latest_csv)}"
    
    success = send_email_with_graph(
        token=GRAPH_TOKEN,
        recipient=TO_EMAIL,
        subject=subject,
        body=body,
        attachment_path=latest_csv
    )
    
    if success:
        print("✅ Test email with attachment sent successfully!")
        return True
    else:
        print("❌ Test email with attachment failed!")
        return False

def main():
    """Main test function"""
    
    print("Starting email system tests...\n")
    
    # Test 1: Basic email
    test1_success = test_email_functionality()
    
    # Test 2: Email with attachment (if available)
    test2_success = test_email_with_attachment()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"   Basic Email Test: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"   Attachment Test:  {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    if test1_success and test2_success:
        print("\n🎉 All email tests passed! The system is ready.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 