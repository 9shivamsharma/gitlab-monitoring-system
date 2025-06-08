#!/bin/bash

# GitLab Monitoring Daily Script
# Runs at 7:30 PM IST daily

# Set the working directory
cd /home/simadmin/gitlab_monitoring_backup

# Create logs directory if it doesn't exist
mkdir -p logs

# Get current date for logging
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_FILE="logs/gitlab_monitoring_$DATE.log"

# Run the monitoring script and log output
echo "=== GitLab Monitoring Started at $(date) ===" >> $LOG_FILE
echo "Working Directory: $(pwd)" >> $LOG_FILE
echo "" >> $LOG_FILE

# Run the Python script
python3 gitlab.py >> $LOG_FILE 2>&1

# Log completion
echo "" >> $LOG_FILE
echo "=== GitLab Monitoring Completed at $(date) ===" >> $LOG_FILE
echo "Generated files:" >> $LOG_FILE
ls -la *.csv >> $LOG_FILE 2>&1

# Get the latest CSV file generated today
LATEST_CSV=$(ls -t gitlab_activity_report_*.csv 2>/dev/null | head -n 1)

if [ -n "$LATEST_CSV" ]; then
    # Send email with CSV attachment using SMTP (reliable, no token expiry!)
    echo "Sending email with attachment: $LATEST_CSV" >> $LOG_FILE
    
    # Get current date and time for email
    CURRENT_DATE=$(date +%Y-%m-%d)
    CURRENT_TIMESTAMP=$(date)
    
    # Create email content
    EMAIL_SUBJECT="GitLab Activity Report - $CURRENT_DATE"
    EMAIL_BODY="Hello,

Please find attached the GitLab activity report generated on $CURRENT_DATE.

Report Details:
- Generated at: $CURRENT_TIMESTAMP  
- Report file: $LATEST_CSV
- Monitoring script completed successfully

Best regards,
GitLab Monitoring System"
    
    # Send email using SMTP (Gmail) - reliable and never expires!
    python3 send_email_smtp.py \
        "$(python3 -c 'from config import FROM_EMAIL; print(FROM_EMAIL)')" \
        "$(python3 -c 'from config import EMAIL_PASSWORD; print(EMAIL_PASSWORD)')" \
        "$(python3 -c 'from config import TO_EMAIL; print(TO_EMAIL)')" \
        "$EMAIL_SUBJECT" \
        "$EMAIL_BODY" \
        "$LATEST_CSV" >> $LOG_FILE 2>&1
    
    if [ $? -eq 0 ]; then
        echo "Email sent successfully via SMTP (Gmail)" >> $LOG_FILE
    else
        echo "Failed to send email via SMTP" >> $LOG_FILE
        echo "Please check your Gmail App Password configuration in config.py" >> $LOG_FILE
    fi
else
    echo "No CSV file found to send" >> $LOG_FILE
fi

echo "GitLab monitoring completed. Check $LOG_FILE for details." 