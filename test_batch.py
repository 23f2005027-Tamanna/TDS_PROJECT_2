import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
# Your Cloud Agent URL (The Solver)
# AGENT_URL = "https://tamannagarg12-tds-quiz-solver.hf.space/solve"
AGENT_URL = "http://localhost:8000/solve"

# The Official Judge (Only works for s-anand.net links)
SUBMIT_URL = "https://tds-llm-analysis.s-anand.net/submit"

# The list of URLs you want to practice with
TEST_URLS = [
    "https://tds-llm-analysis.s-anand.net/demo",
    # "https://tds-llm-analysis.s-anand.net/demo2",
    # "https://p2testingone.vercel.app/q1.html",
    # "https://tdsbasictest.vercel.app/quiz/1"
]

EMAIL = os.getenv("EMAIL")
SECRET = os.getenv("SECRET")

def test_url(url):
    print(f"\n🔗 Testing Target: {url}")
    print(f"   🤖 Agent is thinking... (Timeout: 5 mins)")
    
    try:
        # 1. Send to Agent
        payload = {
            "email": EMAIL,
            "secret": SECRET,
            "url": url
        }
        
        start_time = time.time()
        response = requests.post(AGENT_URL, json=payload, timeout=300)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            # Success!
            data = response.json()
            answer = data.get("answer")
            
            print(f"   ✅ Agent Finished in {duration:.1f}s")
            print(f"   💡 Agent Answer: {answer}")
            
            # 2. Check for the "Old Code" Bug
            if answer == {'status': 'ok'} or answer == "ok":
                print("   ⚠️ WARNING: Agent returned 'ok'. It is running OLD code.")
            
            # 3. Try to Submit (Only for official links)
            if "s-anand.net" in url:
                print("   ⚖️  Verifying with Official Judge...")
                submit_resp = requests.post(SUBMIT_URL, json={
                    "email": EMAIL,
                    "secret": SECRET,
                    "url": url,
                    "answer": answer
                })
                print(f"   📝 Judge Reply: {submit_resp.text}")
            else:
                print("   ℹ️  (External Link: No automatic verification available. Check answer manually.)")
                
        else:
            # Agent Error
            print(f"   ❌ Agent Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"   ❌ Connection Failed: {e}")

if __name__ == "__main__":
    if not EMAIL:
        print("❌ Error: .env file not found or EMAIL missing.")
    else:
        print(f"🚀 Starting Interactive Test Mode")
        for i, link in enumerate(TEST_URLS):
            print(f"\n--- Test {i+1} of {len(TEST_URLS)} ---")
            test_url(link)
            
            if i < len(TEST_URLS) - 1:
                input("\n👉 Press Enter to run the next test...")
        
        print("\n✅ All tests completed.")