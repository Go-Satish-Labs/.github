import json
import os
import requests
from datetime import datetime, timezone

# -----------------------------
# Configuration
# -----------------------------

REPO = os.environ["GITHUB_REPOSITORY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
RESEND_API_KEY = os.environ["RESEND_API_KEY"]

FROM_EMAIL = os.environ["FROM_EMAIL"]

# -----------------------------
# Load team
# -----------------------------

with open("team.json", "r", encoding="utf-8") as file:
    team = json.load(file)["team"]

# -----------------------------
# Date
# -----------------------------

today = datetime.now(timezone.utc).strftime("%d %B %Y")

# -----------------------------
# GitHub Issue
# -----------------------------

issue_title = f"🌅 Analytrix Daily Contribution — {today}"

issue_body = f"""
## 🚀 Analytrix Daily Contribution

**Date:** {today}

This is an automated issue to encourage daily contributions.

Please update your contribution for today.

### 📝 Daily Update

- ✅ What did you complete yesterday?
- 🔨 What are you working on today?
- 🚧 Do you have any blockers?
- 💡 Any ideas or improvements for Analytrix?

### 🎯 Goal

Small contributions every day lead to a stronger Analytrix.

Let's build together. 🚀

---

**This issue was automatically created by GitHub Actions.**
"""

# -----------------------------
# Create GitHub Issue
# -----------------------------

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

issue_url = f"https://api.github.com/repos/{REPO}/issues"

issue_response = requests.post(
    issue_url,
    headers=headers,
    json={
        "title": issue_title,
        "body": issue_body
    },
    timeout=30
)

issue_response.raise_for_status()

issue = issue_response.json()

issue_number = issue["number"]
issue_html_url = issue["html_url"]

print(f"Created issue #{issue_number}")

# -----------------------------
# Assign issue to team
# -----------------------------

assignees = [member["username"] for member in team]

assign_url = (
    f"https://api.github.com/repos/"
    f"{REPO}/issues/{issue_number}/assignees"
)

assign_response = requests.post(
    assign_url,
    headers=headers,
    json={
        "assignees": assignees
    },
    timeout=30
)

if assign_response.ok:
    print("Successfully assigned team members.")
else:
    print(
        "Warning: Could not assign all team members:",
        assign_response.text
    )

# -----------------------------
# Send Emails
# -----------------------------

email_url = "https://api.resend.com/emails"

email_headers = {
    "Authorization": f"Bearer {RESEND_API_KEY}",
    "Content-Type": "application/json"
}

for member in team:

    name = member["name"]
    email = member["email"]

    email_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 650px; margin: auto;">

        <h1>🌅 Good Morning, {name}!</h1>

        <h2>🚀 Analytrix Daily Contribution</h2>

        <p>
            A new day means a new opportunity to contribute,
            improve and build something meaningful.
        </p>

        <hr>

        <h3>📝 Today's Update</h3>

        <ul>
            <li>✅ What did you complete yesterday?</li>
            <li>🔨 What are you working on today?</li>
            <li>🚧 Do you have any blockers?</li>
            <li>💡 Do you have any ideas or improvements?</li>
        </ul>

        <p>
            Please update your contribution in the GitHub issue.
        </p>

        <p>
            <a href="{issue_html_url}"
               style="
               display:inline-block;
               padding:12px 20px;
               background:#24292f;
               color:white;
               text-decoration:none;
               border-radius:6px;">
               Open Daily Contribution
            </a>
        </p>

        <hr>

        <p>
            <strong>Let's build Analytrix together. 🚀</strong>
        </p>

        <p>
            — Analytrix Team
        </p>

    </div>
    """

    payload = {
        "from": FROM_EMAIL,
        "to": [email],
        "subject": f"🌅 Analytrix Daily Contribution — {today}",
        "html": email_body
    }

    response = requests.post(
        email_url,
        headers=email_headers,
        json=payload,
        timeout=30
    )

    if response.ok:
        print(f"Email sent to {name} ({email})")
    else:
        print(
            f"Failed to send email to {name}:",
            response.text
        )
