from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import os

# ⚠️ CRITICAL IMPORT:
# We need the compiled 'agent' object directly to use 'await agent.ainvoke'.
try:
    from agent import agent
except ImportError:
    try:
        from agent import graph as agent
    except ImportError:
        # Fallback for some project structures where it might be named 'app'
        from agent import app as agent

from langchain_core.messages import HumanMessage

load_dotenv()

SECRET = os.getenv("SECRET")
EMAIL = os.getenv("EMAIL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/solve")
async def solve(request: Request):
    # 1. Validate Input
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    if not data or "url" not in data or "secret" not in data:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # 2. Check Security
    if data["secret"] != SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    
    # ✅ FIX: Define task_url here so it is available in the try block
    task_url = data["url"]
    print(f"Verified! Starting task for: {task_url}")

    # 3. Run Agent (WAIT for the answer)
    try:
        # We use 'ainvoke' (Async Invoke) so Playwright doesn't crash the server.
        # This effectively pauses execution here until the agent is DONE thinking.
        response = await agent.ainvoke({
            "messages": [HumanMessage(content=f"Go to this URL and solve the task found there: {task_url}")]
        })
        
        # 4. Extract Answer
        # Iterate backwards to find the last AI message with text content
        final_answer = None
        if "messages" in response:
            for msg in reversed(response["messages"]):
                if msg.type == "ai" and msg.content:
                    final_answer = msg.content
                    break
        
        # Fallback if no specific answer found
        if not final_answer:
            final_answer = "No answer generated."
        
        print(f"Agent Answer: {final_answer}")
        
        # Return the ACTUAL answer to the evaluator (Coordinator)
        return {"answer": final_answer}

    except Exception as e:
        print(f"❌ Error during execution: {e}")
        # Return a 500 error so the client knows something went wrong
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
