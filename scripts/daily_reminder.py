import json
import os
import requests
from datetime import datetime

RESEND_API_KEY = os.environ["RESEND_API_KEY"]
FROM_EMAIL = os.environ["FROM_EMAIL"]

with open("team.json", "r", encoding="utf-8") as f:
    team = json.load(f)["team"]

today = datetime.now().strftime("%d %B %Y")

for member in team:
    name = member["name"]
    email = member["email"]

    payload = {
        "from": FROM_EMAIL,
        "to": [email],
        "subject": f"🌅 Analytrix Daily Reminder — {today}",
        "html": f"""
        <div style="font-family: Arial, sans-serif;">
            <h2>🌅 Good Morning, {name}!</h2>

            <h3>🚀 Analytrix Daily Contribution</h3>

            <p>
                A new day is here. Let's keep Analytrix moving forward.
            </p>

            <p><strong>Please share:</strong></p>

            <ul>
                <li>✅ What did you complete yesterday?</li>
                <li>🔨 What are you working on today?</li>
                <li>🚧 Any blockers?</li>
                <li>💡 Any ideas or improvements?</li>
            </ul>

            <p>
                Every contribution matters. Let's build Analytrix together. 🚀
            </p>

            <br>

            <p>
                — Analytrix Team
            </p>
        </div>
        """
    }

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=30
    )

    if response.ok:
        print(f"✅ Email sent to {name} ({email})")
    else:
        print(f"❌ Failed for {name}: {response.text}")
