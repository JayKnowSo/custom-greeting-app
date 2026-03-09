# Test API Endpoints for Custom Greeting App
# This test script uses the requests library to interact with the API endpoints defined in routes.py.

import json
from urllib import request, parse


print("Starting test script...")

BASE_URL = "http://127.0.0.1:8000"


# --- Helper functions ---
def post_json(url, data):
    data_bytes = json.dumps(data).encode("utf-8")
    req = request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
    with request.urlopen(req) as resp:
        return resp.getcode(), json.load(resp)

def get_json(url, params=None):
    if params:
        query_string = parse.urlencode(params)
        url = f"{url}?{query_string}"
    with request.urlopen(url) as resp:
        return resp.getcode(), json.load(resp)

def print_table(rows, headers):
    # Print headers
    print(" | ".join(headers))
    print("-" * (len(headers) * 15))
    for r in rows:
        print(" | ".join(str(r[h]) for h in headers))
    print("\n")

# --- 0. Clear database ---
# Assuming you have a route to clear all sessions for testing
try:
    status, resp = get_json(f"{BASE_URL}/clear")
    print(f"Database cleared. Status: {status}, Response: {resp}\n")
except Exception:
    print("No clear route found. Continuing without clearing.\n")

# --- Test Data ---
sessions = [
    {"name": "Alice", "greetings": 5, "number": 7, "farewell": "Goodbye!"},
    {"name": "Bob", "greetings": 3, "number": 7, "farewell": "Bye!"},
    {"name": "Charlie", "greetings": 2, "number": 5, "farewell": "See ya!"}
]

# --- 1. Create sessions ---
print("Creating sessions...")
for s in sessions:
    status, resp = post_json(f"{BASE_URL}/session", s)
    print(f"Status: {status}, Response: {resp}")

# --- 2. Search session by name ---
search_name = "Alice"
print(f"\nSearching for sessions with name '{search_name}'...")
status, resp = get_json(f"{BASE_URL}/sessions/search", {"name": search_name})
print(f"Status: {status}")
print_table(resp, ["id", "name", "greetings", "number", "farewell"])

# --- 3. Get stats ---
print("Getting session statistics...")
status, stats = get_json(f"{BASE_URL}/stats")
print(f"Status: {status}")
print(json.dumps(stats, indent=2))


# --- 4. Get all sessions ---
print("\nAll sessions in database:")
status, all_sessions = get_json(f"{BASE_URL}/sessions/search", {"name": ""})  # empty string to fetch all
print_table(all_sessions, ["id", "name", "greetings", "number", "farewell"])

# Note: You can add more tests for edge cases, invalid input, etc.
# For example, test searching for a non-existent name, or creating a session with missing fields.
def main():  # pylint: disable=unused-function

   if __name__ == "__main__":
        main()
