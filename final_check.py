import requests
import json
import os
from dotenv import load_dotenv

# 1. Load the secrets from your .env file
load_dotenv()

# 2. Get the values automatically
MY_EMAIL = os.getenv("EMAIL")
MY_SECRET = os.getenv("SECRET")

# 3. ⚠️ PASTE YOUR HUGGING FACE URL HERE
# Example: "https://tamannagarg12-tds-quiz-solver.hf.space"
CLOUD_URL = "https://tamannagarg12-tds-quiz-solver.hf.space" 

print(f"--- DIAGNOSTIC REPORT ---")
print(f"Loading from .env file...")

# Safety Check: Did it find the secrets?
if not MY_EMAIL or not MY_SECRET:
    print("❌ ERROR: Could not read EMAIL or SECRET from .env")
    print("   Make sure the file exists and is named .env (not .env.txt)")
    exit()

print(f"✅ Found Email: {MY_EMAIL}")
print(f"✅ Found Secret: {MY_SECRET[:2]}*** (Masked)")

payload = {
    "email": MY_EMAIL,
    "secret": MY_SECRET,
    "url": "https://tds-llm-analysis.s-anand.net/demo"
}

print(f"\n🚀 Sending request to: {CLOUD_URL}/solve")

try:
    response = requests.post(
        f"{CLOUD_URL}/solve", 
        json=payload, 
        timeout=120
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! You are ready to submit.")
    elif response.status_code == 403:
        print("\n❌ PASSWORD MISMATCH: The .env on your laptop does not match the Secret on Hugging Face.")

except Exception as e:
    print(f"\n❌ CONNECTION ERROR: {e}")