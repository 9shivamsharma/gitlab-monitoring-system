import requests
import csv
from datetime import datetime, timedelta
from config import API_URL, HEADERS, PROJECTS

# === FUNCTIONS ===

def get_project_members(project_id):
    print(f"  → Fetching members for project ID: {project_id}")
    res = requests.get(f"{API_URL}/projects/{project_id}/members/all", headers=HEADERS)
    print(f"  → Members API response: {res.status_code}")
    if res.status_code == 200:
        members = res.json()
        print(f"  → Found {len(members)} members")
        return members
    else:
        print(f"  → Error getting members: {res.text}")
        return []

def get_user_events(project_id, user_id, after_date):
    print(f"    → Getting events for user {user_id} after {after_date}")
    res = requests.get(
        f"{API_URL}/projects/{project_id}/events",
        headers=HEADERS,
        params={"after": after_date}
    )
    print(f"    → Events API response: {res.status_code}")
    if res.status_code == 200:
        all_events = res.json()
        user_events = [e for e in all_events if e["author_id"] == user_id]
        print(f"    → Found {len(user_events)} events for this user")
        return user_events
    else:
        print(f"    → Error getting events: {res.text}")
        return []

# === MAIN ===
def generate_report():
    report_data = []
    last_week = (datetime.now() - timedelta(days=7)).date().isoformat()
    print(f"Looking for activity after: {last_week}")

    for project in PROJECTS:
        project_name = project["name"]
        project_id = project["id"]
        
        print(f"\n🔍 Processing project: {project_name} (ID: {project_id})")

        members = get_project_members(project_id)
        
        if not members:
            print(f"  ⚠️ No members found for {project_name}")
            continue
            
        for member in members:
            user_id = member["id"]
            username = member["username"]
            name = member["name"]
            
            print(f"  👤 Checking user: {name} (@{username})")

            events = get_user_events(project_id, user_id, last_week)
            latest_event = max(events, key=lambda e: e["created_at"], default=None)

            if latest_event:
                print(f"    ✅ Latest activity: {latest_event['action_name']}")
                report_data.append([
                    name,
                    project_name,
                    latest_event["action_name"].capitalize(),
                    latest_event["created_at"]
                ])
            else:
                print(f"    ❌ No recent activity")
                report_data.append([name, project_name, "No Activity", ""])

    print(f"\n📊 Total report entries: {len(report_data)}")
    
    # Save as CSV
    today = datetime.now().date().isoformat()
    filename = f"gitlab_activity_report_{today}.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["#", "Developer Name", "Project", "Latest Activity", "Activity Timestamp"])
        for idx, row in enumerate(report_data, start=1):
            writer.writerow([idx] + row)

    print(f"✅ Report saved: {filename}")
    
    if len(report_data) == 0:
        print("⚠️ No data was collected. Check the debugging output above.")

if __name__ == "__main__":
    generate_report()
