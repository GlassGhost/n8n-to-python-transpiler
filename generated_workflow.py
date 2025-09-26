# Set Name
name = "Alice"

# If Name Check
if name == Alice:
    print("Condition met")
else:
    print("Condition not met")

# Delay Node
import time

print("Delaying for 2 seconds...")
time.sleep(2)

# Send Slack Message
import requests

payload = {"text": "Hello, Alice!"}
response = requests.post(
    "https://hooks.slack.com/services/YOUR/WEBHOOK/URL", json=payload
)
print(response.status_code)

# Sticky Note
# This is a test comment.
