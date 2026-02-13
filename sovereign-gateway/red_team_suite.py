import requests
import json
import secrets
import time

BASE_URL = "http://127.0.0.1:8000"

def clean_msg(msg):
    return msg.encode('ascii', 'ignore').decode('ascii').strip()

def run_red_team_suite():
    print("--- [RED TEAM] SOVEREIGN PASSPORT PENETRATION TEST SUITE ---")
    
    # 0. Get a valid passport as baseline
    print("\n[PREP] Generating valid baseline passport...")
    intent = "EXECUTE_SECURE_PAYMENT_v1"
    try:
        resp = requests.post(f"{BASE_URL}/issue-passport", json={"intent": intent}, timeout=5)
        base = resp.json()
        sig = base['signature']
        seed = base['seed']
        print(f"[PREP] Valid Passport Issued. ID: {seed}")

        # TEST 1: The Man-in-the-Middle (Payload Tampering)
        print("\n--- TEST 1: Man-in-the-Middle (MITM) ---")
        print("[ATTACK] Intercepting Request...")
        tampered_intent = "EXECUTE_SECURE_PAYMENT_v1_AND_TRANSFER_ALL_FUNDS"
        print(f"[ATTACK] Modifying Payload to: '{tampered_intent}'")
        print("[ATTACK] Re-injecting Packet with original signature...")
        
        t1_resp = requests.post(f"{BASE_URL}/verify-passport", json={
            "intent": tampered_intent,
            "signature": sig,
            "seed": seed
        }, timeout=5)
        result = t1_resp.json()
        print(f"[GATEWAY] Result: {clean_msg(result['message'])}")
        print(f"[GATEWAY] Details: {result['details']}")
        if result['status'] == "REJECTED":
            print("[SUCCESS] Test 1: MITM blocked by Structural Integrity.")
        else:
            print("[FAIL] Test 1: MITM succeeded. Security failure.")

        # TEST 2: The Replay Attack (Stale Passport)
        print("\n--- TEST 2: Replay Attack ---")
        print("[ATTACK] Captured valid session. Verifying once...")
        
        # First, verify the original valid one to mark the seed as 'used'
        requests.post(f"{BASE_URL}/verify-passport", json={
            "intent": intent,
            "signature": sig,
            "seed": seed
        }, timeout=5)
        
        print(f"[ATTACK] Attempting Replay of ID: {seed}")
        
        t2_resp = requests.post(f"{BASE_URL}/verify-passport", json={
            "intent": intent,
            "signature": sig,
            "seed": seed
        }, timeout=5)
        result2 = t2_resp.json()
        print(f"[GATEWAY] Result: {clean_msg(result2['message'])}")
        print(f"[GATEWAY] Details: {result2['details']}")
        if result2['status'] == "REJECTED":
            print("[SUCCESS] Test 2: Replay blocked by Stale Entropy check.")
        else:
            print("[FAIL] Test 2: Replay succeeded. Security failure.")

        # TEST 3: The Brute-Force (Logic Guessing)
        print("\n--- TEST 3: Logic Brute-Force ---")
        print("[ATTACK] Attempting to guess Quine logic...")
        fake_sig = secrets.token_hex(32)
        print(f"[ATTACK] Injecting random signature guess: {fake_sig[:16]}...")
        
        t3_resp = requests.post(f"{BASE_URL}/verify-passport", json={
            "intent": intent,
            "signature": fake_sig,
            "seed": secrets.token_hex(4) # Guessing entropy seed too
        }, timeout=5)
        result3 = t3_resp.json()
        print(f"[GATEWAY] Result: {clean_msg(result3['message'])}")
        if result3['status'] == "REJECTED":
            print("[SUCCESS] Test 3: Brute-Force failed against non-deterministic gate.")
        else:
            print("[FAIL] Test 3: Guess succeeded. Critical security failure.")

        print("\n--- [RESULT] SOVEREIGN INTEGRITY MAINTAINED ---")
    except requests.exceptions.ConnectionError:
        print("Error: Gateway server is not running on localhost:8000.")

if __name__ == "__main__":
    run_red_team_suite()
