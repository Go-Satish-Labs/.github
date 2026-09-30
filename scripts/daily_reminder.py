import json
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# ==========================================
# Configuration
# ==========================================

GMAIL_USERNAME = os.getenv("GMAIL_USERNAME")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

if not GMAIL_USERNAME:
    print("❌ ERROR: GMAIL_USERNAME is not configured.")
    sys.exit(1)

if not GMAIL_APP_PASSWORD:
    print("❌ ERROR: GMAIL_APP_PASSWORD is not configured.")
    sys.exit(1)


# ==========================================
# Load team
# ==========================================

try:
    with open("team.json", "r", encoding="utf-8") as file:
        team = json.load(file)["team"]

except Exception as e:
    print(f"❌ ERROR: Could not read team.json: {e}")
    sys.exit(1)


if not team:
    print("❌ ERROR: No team members found.")
    sys.exit(1)


# ==========================================
# Date
# ==========================================

today = datetime.now().strftime("%d %B %Y")


# ==========================================
# Email server
# ==========================================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# ==========================================
# Counters
# ==========================================

success_count = 0
failed_count = 0


print("")
print("=" * 60)
print("🚀 ANALYTRIX DAILY REMINDER")
print("=" * 60)
print(f"📅 Date: {today}")
print(f"📧 Sender: {GMAIL_USERNAME}")
print(f"👥 Recipients: {len(team)}")
print("=" * 60)
print("")


# ==========================================
# Connect to Gmail
# ==========================================

try:

    print("🔐 Connecting to Gmail SMTP...")

    server = smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT,
        timeout=30
    )

    server.ehlo()

    server.starttls()

    server.ehlo()

    server.login(
        GMAIL_USERNAME,
        GMAIL_APP_PASSWORD
    )

    print("✅ Gmail authentication successful.")
    print("")

except Exception as e:

    print("❌ Gmail authentication failed.")
    print(f"Error: {e}")

    sys.exit(1)


# ==========================================
# Send emails
# ==========================================

for member in team:

    name = member.get("name")
    email = member.get("email")

    if not name or not email:

        print("⚠️ Invalid team member:")
        print(member)

        failed_count += 1
        continue


    # --------------------------------------
    # Email body
    # --------------------------------------

    html_body = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>
Analytrix Daily Reminder
</title>

</head>


<body style="
margin:0;
padding:0;
background:#f4f4f4;
font-family:Arial,Helvetica,sans-serif;
">


<div style="
max-width:650px;
margin:40px auto;
background:#ffffff;
padding:40px;
border-radius:12px;
">


<h1 style="
margin-top:0;
">
🌅 Good Morning, {name}!
</h1>


<h2>
🚀 Analytrix Daily Contribution
</h2>


<p>
A new day means a new opportunity to contribute,
learn, improve, and build Analytrix together.
</p>


<hr>


<h3>
📝 Today's Contribution
</h3>


<p>
Please share your update for today:
</p>


<ul>

<li>
✅ What did you complete yesterday?
</li>

<li>
🔨 What are you working on today?
</li>

<li>
🚧 Do you have any blockers?
</li>

<li>
💡 Do you have any ideas or improvements?
</li>

</ul>


<h3>
🎯 Daily Goal
</h3>


<p>
Every contribution matters.
Even a small contribution moves Analytrix forward.
</p>


<p>
Let's keep building together. 🚀
</p>


<hr>


<p>
<strong>
Analytrix Team
</strong>
</p>


<p style="color:#777;">
This is an automated daily reminder.
</p>


</div>


</body>

</html>
"""


    # --------------------------------------
    # Create email
    # --------------------------------------

    message = MIMEMultipart("alternative")

    message["From"] = GMAIL_USERNAME
    message["To"] = email
    message["Subject"] = (
        f"🌅 Analytrix Daily Reminder — {today}"
    )


    # Plain-text fallback

    text_body = f"""
Good Morning, {name}!

🚀 Analytrix Daily Contribution

Please share your update for today:

✅ What did you complete yesterday?
🔨 What are you working on today?
🚧 Any blockers?
💡 Any ideas or improvements?

Every contribution matters.

Let's keep building Analytrix together. 🚀

— Analytrix Team
"""


    message.attach(
        MIMEText(text_body, "plain", "utf-8")
    )

    message.attach(
        MIMEText(html_body, "html", "utf-8")
    )


    # --------------------------------------
    # Send
    # --------------------------------------

    try:

        server.sendmail(
            GMAIL_USERNAME,
            email,
            message.as_string()
        )

        print(
            f"✅ Email sent to "
            f"{name} <{email}>"
        )

        success_count += 1

    except Exception as e:

        print(
            f"❌ Failed to send to "
            f"{name} <{email}>"
        )

        print(f"   Error: {e}")

        failed_count += 1


# ==========================================
# Close Gmail connection
# ==========================================

try:

    server.quit()

    print("")
    print("🔌 Gmail connection closed.")

except Exception:
    pass


# ==========================================
# Summary
# ==========================================

print("")
print("=" * 60)
print("📊 EMAIL SUMMARY")
print("=" * 60)

print(
    f"✅ Successfully sent: {success_count}"
)

print(
    f"❌ Failed:            {failed_count}"
)

print(
    f"👥 Total members:     {len(team)}"
)

print("=" * 60)


# ==========================================
# Fail GitHub Action if necessary
# ==========================================

if failed_count > 0:

    print("")
    print(
        "❌ Workflow failed because "
        "one or more emails could not be sent."
    )

    sys.exit(1)


print("")
print(
    "🎉 All Analytrix emails were sent successfully!"
)
print("")
