import requests
from config import HEADERS

def test_api_access():
    """Test if the API token is working"""
    print("Testing API access...")
    res = requests.get(f"https://gitlab.com/api/v4/user", headers=HEADERS)
    if res.status_code == 200:
        user_info = res.json()
        print(f"✅ Token is valid. Logged in as: {user_info['name']} (@{user_info['username']})")
        return True
    else:
        print(f"❌ Token validation failed: {res.status_code}")
        print(f"Response: {res.text}")
        return False

def list_all_projects():
    """Try different ways to list projects"""
    if not test_api_access():
        return
    
    print("\n" + "=" * 60)
    print("Trying different methods to list projects...")
    
    # Method 1: List all accessible projects with pagination
    print("\n1. Listing all accessible projects:")
    all_projects = []
    page = 1
    per_page = 100
    
    while True:
        res = requests.get(f"https://gitlab.com/api/v4/projects", 
                          headers=HEADERS, 
                          params={"page": page, "per_page": per_page})
        if res.status_code == 200:
            projects = res.json()
            if not projects:  # No more projects
                break
            all_projects.extend(projects)
            page += 1
        else:
            print(f"❌ Failed: {res.status_code} - {res.text}")
            break
    
    if all_projects:
        print(f"Found {len(all_projects)} total accessible projects:")
        for project in all_projects:
            print(f"  - {project['name']} (ID: {project['id']})")
    
    # Method 2: Try to get group projects (if simplyfiitsupport is a group)
    print("\n2. Trying to list group projects:")
    res = requests.get(f"https://gitlab.com/api/v4/groups/simplyfiitsupport/projects", headers=HEADERS)
    if res.status_code == 200:
        projects = res.json()
        print(f"Found {len(projects)} group projects:")
        for project in projects:
            print(f"  - {project['name']} (ID: {project['id']})")
    else:
        print(f"❌ Failed: {res.status_code} - {res.text}")
    
    # Method 3: Search for projects
    print("\n3. Searching for projects:")
    res = requests.get(f"https://gitlab.com/api/v4/projects", headers=HEADERS, params={"search": "Climate"})
    if res.status_code == 200:
        projects = res.json()
        print(f"Found {len(projects)} projects matching 'Climate':")
        for project in projects:
            print(f"  - {project['name']} (ID: {project['id']})")
    else:
        print(f"❌ Failed: {res.status_code} - {res.text}")

if __name__ == "__main__":
    list_all_projects() 