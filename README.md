# GitLab Monitoring System

## Overview
A complete GitLab monitoring system that tracks developer activity across multiple projects and generates daily CSV reports.

## Features
- ✅ Monitors 32 developers across 7 GitLab projects
- ✅ Generates daily CSV reports with activity tracking
- ✅ Automated execution at 8:00 PM IST daily
- ✅ Detailed logging system
- ✅ 7-day activity window monitoring
- ✅ **Email functionality** - Automatically sends reports via Microsoft Graph API

## Files Structure

| File | Description |
|------|-------------|
| `gitlab.py` | Main monitoring script that fetches developer activity |
| `run_gitlab_monitoring.sh` | Shell script for automated daily execution |
| `list_projects.py` | Utility to discover and list accessible GitLab projects |
| `send_email_graph.py` | Email functionality using Microsoft Graph API |
| `test_email.py` | Test script for email functionality |
| `config.py` | Configuration file with tokens and project settings |
| `config.example.py` | Example configuration file (safe to share) |
| `logs/` | Directory containing execution logs |
| `gitlab_activity_report_*.csv` | Daily generated CSV reports |

## Security

🔒 **This repository uses secure configuration management:**
- Access tokens are **NOT** stored in code
- Use environment variables or a local `config.py` file
- The `config.py` file is git-ignored for security
- Copy `config.example.py` to `config.py` and add your credentials

## Dependencies
- Python 3
- `requests` library: `pip install requests`
- Linux/Unix system with cron support

## Setup Instructions

### 1. Install Dependencies
```bash
pip install requests
```

### 2. Configure Tokens
```bash
# Copy the example configuration
cp config.example.py config.py

# Edit config.py and add your tokens:
# - GitLab Personal Access Token
# - Microsoft Graph Token (for email functionality)
# - Update email addresses

# OR set environment variables (recommended)
export GITLAB_TOKEN=your_gitlab_token_here
export GRAPH_TOKEN=your_graph_token_here
```

### 3. Set Permissions
```bash
chmod +x run_gitlab_monitoring.sh
```

### 4. Test the System
```bash
python3 gitlab.py
```

### 5. Setup Daily Automation (Optional)
```bash
crontab -e
# Add this line for daily execution at 8:00 PM IST:
0 20 * * * /path/to/your/gitlab_monitoring/run_gitlab_monitoring.sh
```

## Configuration

### Monitored Projects
The system currently monitors these 7 projects:
- climate_sense_AI (ID: 67898103)
- direct-import (ID: 70317710)
- Avatar (ID: 66858690)
- cyberGPT_2.0 (ID: 65812465)
- CyberGPT-2.0 (ID: 69870213)
- tbml-frontend (ID: 70051907)
- tbml (ID: 70078187)

### Settings
- **Execution Time**: 8:00 PM IST daily
- **Activity Window**: Last 7 days
- **Output Format**: CSV with timestamps
- **Developers Tracked**: 32 team members

## Usage

### Manual Execution
```bash
python3 gitlab.py
```

### View Logs
```bash
ls logs/
cat logs/gitlab_monitoring_YYYY-MM-DD_HH-MM-SS.log
```

### Check Generated Reports
```bash
ls gitlab_activity_report_*.csv
```

### Test Email Functionality
```bash
python3 test_email.py
```

### Send Report via Email
```bash
python3 send_email_graph.py recipient@domain.com "GitLab Report" "Please find attached report" report.csv
```

## Output Files
- **CSV Reports**: `gitlab_activity_report_YYYY-MM-DD.csv`
- **Execution Logs**: `logs/gitlab_monitoring_YYYY-MM-DD_HH-MM-SS.log`

## Troubleshooting

### Common Issues
1. **Token expired**: Update the `PRIVATE_TOKEN` in `gitlab.py`
2. **Permission denied**: Ensure the token has appropriate project access
3. **No data**: Check project IDs and user permissions

### Testing Tools
- Use `list_projects.py` to discover available projects
- Check logs for detailed execution information

## Support
This system has been tested and works for monitoring 32 developers across 7 GitLab projects with daily automated reporting. 