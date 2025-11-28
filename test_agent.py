import requests
import json
import os

# 1. Load your secrets manually (or ensure they are in .env)
# REPLACE THESE WITH YOUR EXACT VALUES FROM YOUR .ENV FILE
MY_EMAIL = os.getenv("EMAIL")
MY_SECRET = os.getenv("SECRET") 

# 2. Define the payload
payload = {
    "email": MY_EMAIL,
    "secret": MY_SECRET,
    "url": "https://tds-llm-analysis.s-anand.net/demo"
}

# 3. Send the request to your local server
print(f"🚀 Sending request to server...")
try:
    response = requests.post("http://localhost:7860/solve", json=payload)
    
    # 4. Print the result
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(response.text)
    
except Exception as e:
    print(f"❌ Failed to connect: {e}")
    print("Make sure 'python main.py' is still running in the other terminal!")