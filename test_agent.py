import requests
import json
import os

# Load secrets from .env, don't type them manually

# Configuration
CLOUD_URL = "https://tamannagarg12-tds-quiz-solver.hf.space"
# REPLACE THESE WITH YOUR EXACT VALUES FROM YOUR .ENV FILE
MY_EMAIL = os.getenv("EMAIL")
MY_SECRET = os.getenv("SECRET") 

# 2. Define the payload
payload = {
    "email": MY_EMAIL,
    "secret": MY_SECRET,
    "url": "https://tds-llm-analysis.s-anand.net/demo"
}

print(f"🚀 Sending request to: {CLOUD_URL}/solve")

try:
    # We use requests.post(..., json=payload) which AUTOMATICALLY fixes JSON formatting errors
    response = requests.post(f"{CLOUD_URL}/solve", json=payload, timeout=120)
    
    print(f"\nStatus Code: {response.status_code}")
    print("Response:")
    print(response.text)

except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure 'python main.py' is still running in the other terminal!")