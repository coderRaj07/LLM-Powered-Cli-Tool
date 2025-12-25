import json
import os
import random
from pathlib import Path
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

from formbricks.llm_json import parse_llm_json

load_dotenv()

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# ---------------- JSON SANITIZER ----------------

def strip_json_fences(content: str) -> str:
    if not content:
        return ""

    content = content.strip()

    # Remove starting ``` or ```json
    if content.startswith("```"):
        content = content.lstrip("`").strip()
        if content.lower().startswith("json"):
            content = content[4:].strip()

    # Remove ending ```
    if content.endswith("```"):
        content = content.rstrip("`").strip()

    return content


# ---------------- PROMPTS ----------------

USERS_PROMPT = """
You are generating workspace users for a self-hosted Formbricks instance.

Rules:
- Output ONLY valid JSON
- No markdown, no explanation
- Use realistic professional names and company emails
- These are INTERNAL dashboard users (not survey respondents)

Each user must include:
- id (string, uuid-like)
- name (string)
- email (string)
- role (owner, manager, member)
- isActive (boolean)
- teams (empty array)

Generate exactly 20 users:
- 1 owner
- 9 managers
- 10 members

Use this exact JSON format:

{
  "users": [
    {
      "id": "u_1a2b3c",
      "name": "John Doe",
      "email": "john@company.com",
      "role": "member",
      "isActive": true,
      "teams": []
    }
  ]
}
"""

SURVEYS_PROMPT = """
You are generating realistic surveys for a self-hosted Formbricks instance.

Rules:
- Output ONLY valid JSON
- No markdown, no explanation, no comments
- Professional SaaS surveys only
- Do NOT ask for names, emails, phone numbers, or personal identifiers

Survey rules:
- Generate exactly 5 surveys
- Each survey must have 7–9 questions
- Each survey must have a clear theme

Question rules:
- id MUST be q1, q2, q3...
- type MUST be:
  - openText
  - multipleChoiceSingle
  - multipleChoiceMulti
- headline MUST be:
  { "default": "Question text" }
- required MUST be boolean

Multiple choice rules:
- choices MUST be objects with id + label.default
- ALWAYS include "shuffleOption": "none"

Allowed fields ONLY:
- name
- status
- type
- questions

Use EXACT structure:

{
  "surveys": [
    {
      "name": "Survey name",
      "status": "inProgress",
      "type": "link",
      "questions": []
    }
  ]
}
"""

RESPONSE_PROMPT_TEMPLATE = """
You are answering a professional SaaS survey as a real user.

Context:
- You are a team member using a SaaS product
- Answer honestly and consistently
- Professional, natural language

Rules:
- Output ONLY valid JSON
- Answer ALL questions
- For multipleChoiceSingle → return ONE option label
- For multipleChoiceMulti → return ARRAY of option labels
- Use option labels EXACTLY as given

Survey name: {survey_name}

Questions:
{questions_json}

Return EXACT format:
{{
  "answers": {{
    "q1": "...",
    "q2": "...",
    "q3": ["...", "..."]
  }}
}}
"""


# ---------------- GENERATORS ----------------
def generate_users(client):
    def call():
        resp = client.chat.completions.create(
            model="llama-3.3-70b",
            messages=[{"role": "user", "content": USERS_PROMPT}],
            temperature=0.2,
            max_completion_tokens=2048,
        )
        return resp.choices[0].message.content

    data = parse_llm_json(call, label="users")
    return data["users"]


def generate_surveys(client):
    def call():
        resp = client.chat.completions.create(
            model="llama-3.3-70b",
            messages=[{"role": "user", "content": SURVEYS_PROMPT}],
            temperature=0.2,
            max_completion_tokens=4096,
        )
        return resp.choices[0].message.content

    data = parse_llm_json(call, label="surveys")
    return data["surveys"]


def generate_responses(client, members, surveys):
    responses = []

    for user in members:
        selected_surveys = random.sample(
            surveys,
            k=random.randint(1, 2)
        )

        for survey in selected_surveys:
            prompt = RESPONSE_PROMPT_TEMPLATE.format(
                survey_name=survey["name"],
                questions_json=json.dumps(survey["questions"], indent=2)
            )

            def call():
                resp = client.chat.completions.create(
                    model="llama-3.3-70b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_completion_tokens=1024,
                )
                return resp.choices[0].message.content

            try:
                parsed = parse_llm_json(
                    call,
                    label=f"response_{user['id']}_{survey['name']}"
                )
            except RuntimeError:
                print("Skipping invalid response")
                continue

            responses.append({
                "userId": user["id"],
                "survey": survey["name"],
                "answers": parsed["answers"]
            })

    return responses

# ---------------- MAIN ----------------

def generate():
    print("Generating seed data with Cerebras...")
    client = Cerebras(api_key=os.environ["CEREBRAS_API_KEY"])

    users = generate_users(client)
    surveys = generate_surveys(client)

    internal_users = [u for u in users if u["role"] in ("owner", "manager")]
    members = [u for u in users if u["role"] == "member"]

    assert len(internal_users) == 10, "Internal users must be exactly 10"
    assert len(members) == 10, "Members must be exactly 10"

    responses = generate_responses(client, members, surveys)

    (DATA_DIR / "users.json").write_text(json.dumps(users, indent=2))
    (DATA_DIR / "surveys.json").write_text(json.dumps(surveys, indent=2))
    (DATA_DIR / "responses.json").write_text(json.dumps(responses, indent=2))

    print("users.json, surveys.json, responses.json generated")
    print(f"Internal users: {len(internal_users)}")
    print(f"Respondents: {len(members)}")
    print(f"Responses: {len(responses)}")


if __name__ == "__main__":
    generate()
