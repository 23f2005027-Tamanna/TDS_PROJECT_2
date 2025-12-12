import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---

# 1. Your Agent (The Solver) - UPDATE THIS with your Hugging Face URL if needed
# Use the cloud URL for the final test.
AGENT_URL = "https://tamannagarg12-tds-quiz-solver.hf.space/solve" 
# Or use localhost if testing locally: "http://localhost:8000/solve"

# 2. The Game Server (The Judge)
SUBMIT_URL = "https://tds-llm-analysis.s-anand.net/submit"

# 3. Starting Level (The Mock Test Entry Point)
START_URL = "https://tds-llm-analysis.s-anand.net/project2"

# Get credentials from .env
EMAIL = os.getenv("EMAIL")
SECRET = os.getenv("SECRET")

def solve_level(current_task_url):
    print(f"\n🔍 --- New Level: {current_task_url} ---")
    
    # PHASE 1: Ask your Agent to solve it
    print(f"   🤖 Agent is thinking...")
    try:
        agent_payload = {
            "email": EMAIL,
            "secret": SECRET,
            "url": current_task_url
        }
        # Call your Agent. Increased timeout to 300s (5 mins) for complex tasks.
        agent_resp = requests.post(AGENT_URL, json=agent_payload, timeout=300)
        
        if agent_resp.status_code != 200:
            print(f"   ❌ Agent Failed (Status {agent_resp.status_code})")
            print(f"   Error: {agent_resp.text}")
            return None

        # Extract the answer from your agent's response
        agent_data = agent_resp.json()
        
        # Look for the answer in common keys
        answer = agent_data.get("answer") or agent_data.get("result") or agent_data
        
        print(f"   💡 Agent suggests: {answer}")
        return answer

    except Exception as e:
        print(f"   ❌ Connection Error to Agent: {e}")
        return None

def submit_answer(task_url, answer):
    # PHASE 2: Submit to the Judge
    print(f"   submission -> Sending to Judge...")
    
    submit_payload = {
        "email": EMAIL,
        "secret": SECRET,
        "url": task_url,
        "answer": answer
    }
    
    try:
        judge_resp = requests.post(SUBMIT_URL, json=submit_payload)
        
        if judge_resp.status_code == 200:
            result = judge_resp.json()
            is_correct = result.get("correct", False)
            
            # ✅ FIX: Check for both 'nextURL' and 'url' (some servers use different keys)
            next_url = result.get("nextURL") or result.get("url")
            
            if is_correct:
                print(f"   ✅ CORRECT! (Judge said: {result.get('message', 'Good job')})")
                return next_url
            else:
                print(f"   ❌ WRONG ANSWER. (Judge said: {result.get('message')})")
                return None
        else:
            print(f"   ⚠️ Submission Error: {judge_resp.status_code}")
            print(judge_resp.text)
            return None
            
    except Exception as e:
        print(f"   ❌ Connection Error to Judge: {e}")
        return None

# --- MAIN GAME LOOP ---
def main():
    current_url = START_URL
    
    while current_url:
        # 1. Solve
        answer = solve_level(current_url)
        if not answer:
            print("   🛑 Stopping due to Agent error or empty answer.")
            break
            
        # 2. Submit
        next_level = submit_answer(current_url, answer)
        
        # 3. Transition
        if next_level:
            current_url = next_level
            print("   🚀 Moving to next level in 3 seconds...")
            time.sleep(3)
        else:
            print("\n🏁 Game Over (Either finished or stuck).")
            break

if __name__ == "__main__":
    if not EMAIL or not SECRET:
        print("❌ ERROR: EMAIL or SECRET is missing from .env file.")
    else:
        main()