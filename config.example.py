import os

# GitLab Configuration
GITLAB_BASE_URL = "https://gitlab.com"
API_URL = f"{GITLAB_BASE_URL}/api/v4"

# Get token from environment variable or replace 'your-token-here' with your actual token
PRIVATE_TOKEN = os.environ.get('GITLAB_TOKEN', 'your-token-here')
HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

# Projects with names and IDs for monitoring
# Update these with your actual project IDs
PROJECTS = [
    {"name": "project1", "id": 12345678},
    {"name": "project2", "id": 87654321},
    # Add more projects as needed
]

# Microsoft Graph Configuration for Email (Optional)
GRAPH_TOKEN = os.environ.get('GRAPH_TOKEN', 'your-graph-token-here')

# Email Configuration (Update with your emails)
FROM_EMAIL = "your-sender@domain.com"
TO_EMAIL = "your-recipient@domain.com"

# Email Template Settings
EMAIL_SUBJECT_TEMPLATE = "GitLab Activity Report - {date}"
EMAIL_BODY_TEMPLATE = """Hello,

Please find attached the GitLab activity report generated on {date}.

Report Details:
- Generated at: {timestamp}
- Report file: {filename}
- Monitoring script completed successfully

Best regards,
GitLab Monitoring System
"""

# Helper functions for email
def get_email_body(date, timestamp, filename):
    return EMAIL_BODY_TEMPLATE.format(
        date=date,
        timestamp=timestamp,
        filename=filename
    )

def get_email_subject(date):
    return EMAIL_SUBJECT_TEMPLATE.format(date=date)

# Instructions:
# 1. Copy this file to config.py
# 2. Replace 'your-token-here' with your GitLab Personal Access Token
# 3. Replace 'your-graph-token-here' with your Microsoft Graph token (for email)
# 4. Update email addresses in FROM_EMAIL and TO_EMAIL
# 5. Update the PROJECTS list with your actual project names and IDs
# 6. Or set environment variables: 
#    export GITLAB_TOKEN=your_gitlab_token
#    export GRAPH_TOKEN=your_graph_token 