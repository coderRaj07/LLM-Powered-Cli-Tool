import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path("data")

API_URL = os.environ["FORMBRICKS_API_URL"]
API_KEY = os.environ["FORMBRICKS_API_KEY"]
ORG_ID = os.environ["FORMBRICKS_ORG_ID"]
ENV_ID = os.environ["FORMBRICKS_ENV_ID"]

# -------- HEADERS --------

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}

# ---------------- USERS (v2) ----------------

def seed_users():
    users_path = DATA_DIR / "users.json"
    if not users_path.exists():
        print("users.json not found")
        return

    users = json.loads(users_path.read_text())
    print("Seeding users (v2)...")

    for user in users:
        payload = {
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "isActive": user.get("isActive", True),
            "teams": user.get("teams", []),
        }

        resp = requests.post(
            f"{API_URL}/api/v2/organizations/{ORG_ID}/users",
            headers=HEADERS,
            json=payload,
        )

        if resp.status_code in (200, 201):
            print(f"User created: {user['email']} ({user['role']})")
        elif resp.status_code == 409:
            print(f"User already exists: {user['email']}")
        else:
            print(f"User failed ({user['email']}): {resp.text}")

# ---------------- SURVEYS (v1) ----------------

def seed_surveys():
    surveys_path = DATA_DIR / "surveys.json"
    if not surveys_path.exists():
        print("surveys.json not found. Run generate() first.")
        return {}

    surveys = json.loads(surveys_path.read_text())
    survey_map = {}

    print("Seeding surveys (v1)...")

    for survey in surveys:
        payload = {
            "environmentId": ENV_ID,
            "name": survey["name"],
            "status": survey["status"],
            "type": survey["type"],
            "questions": survey["questions"],
        }

        resp = requests.post(
            f"{API_URL}/api/v1/management/surveys",
            headers=HEADERS,
            json=payload,
        )

        if resp.status_code in (200, 201):
            data = resp.json().get("data", {})
            survey_id = data.get("id")
            survey_map[survey["name"]] = survey_id
            print(f"Survey created: {survey['name']}")
        else:
            print(f"Survey failed ({survey['name']}): {resp.text}")

    return survey_map

# ---------------- RESPONSES (v1 client) ----------------

def seed_responses(survey_map):
    responses_path = DATA_DIR / "responses.json"
    if not responses_path.exists():
        print("No responses.json found, skipping responses")
        return

    responses = json.loads(responses_path.read_text())
    print("Seeding responses (client API)...")

    for resp_data in responses:
        survey_name = resp_data["survey"]
        survey_id = survey_map.get(survey_name)

        if not survey_id:
            print(f"Survey not found for response: {survey_name}")
            continue

        payload = {
            "surveyId": survey_id,
            "data": resp_data["answers"],
            "finished": True
        }

        resp = requests.post(
            f"{API_URL}/api/v1/client/{ENV_ID}/responses",
            headers={"Content-Type": "application/json"},
            json=payload,
        )

        if resp.status_code in (200, 201):
            print(f"Response seeded for {survey_name}")
        else:
            print(f"Response failed ({survey_name}): {resp.text}")

# ---------------- MAIN ----------------

def seed():
    seed_users()
    survey_map = seed_surveys()
    seed_responses(survey_map)
    print("------All seeding complete!-------")

if __name__ == "__main__":
    seed()
