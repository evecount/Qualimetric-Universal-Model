from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import hashlib
import json
import requests
import secrets
import uvicorn

import os

app = FastAPI()

# Resolve paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static files for CSS/JS
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Replay Protection: Tracking processed seeds
used_seeds = set()

def get_quantum_entropy():
    """Fetches live quantum entropy from ANU API or simulates if offline."""
    try:
        response = requests.get("https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint16", timeout=5)
        if response.status_code == 200:
            return str(response.json()['data'][0])
    except:
        pass
    return secrets.token_hex(8)

def generate_structural_signature(intent_data, quantum_seed, iterations=2):
    """
    The 'USP': Binds Qualitative Intent to Hardware-Rooted Truth.
    Produces a self-referential Structural Signature (SHA3-256).
    """
    # Step 1: Serialize the 'Intent' (The Passport Body)
    passport_body = json.dumps(intent_data, sort_keys=True)
    
    # Step 2: Initialize the Quine with the Quantum Entropy Seed
    current_state = f"{passport_body}|{quantum_seed}"
    
    # Step 3: Recursive Hash Loop
    for i in range(iterations):
        structural_layer = hashlib.sha3_256(current_state.encode()).hexdigest()
        current_state = f"{structural_layer}:{current_state}"
    
    return hashlib.sha3_256(current_state.encode()).hexdigest()

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/issue-passport")
async def issue_passport(request: Request):
    data = await request.json()
    intent = data.get("intent")
    seed = get_quantum_entropy()
    signature = generate_structural_signature(intent, seed)
    return {
        "signature": signature, 
        "seed": seed, 
        "intent": intent,
        "status": "ISSUED"
    }

@app.post("/verify-passport")
async def verify_passport(request: Request):
    data = await request.json()
    intent = data.get("intent")
    signature = data.get("signature")
    seed = data.get("seed")
    
    # Check for Replay Attack
    if seed in used_seeds:
        return {
            "status": "REJECTED", 
            "message": "❌ ACCESS DENIED: Stale Entropy Seed Detected.",
            "details": "This passport signature has already been used (Replay Attack)."
        }
    
    expected = generate_structural_signature(intent, seed)
    
    if signature == expected:
        used_seeds.add(seed) # Commit seed to history on success
        return {
            "status": "VERIFIED", 
            "message": "✅ ACCESS GRANTED: Sovereign Integrity Verified.",
            "details": "Structure identical to quantum-anchored truth."
        }
    else:
        return {
            "status": "REJECTED", 
            "message": "❌ ACCESS DENIED: Structural Signature Mismatch.",
            "details": "Potential Hallucination or Tampering detected."
        }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
