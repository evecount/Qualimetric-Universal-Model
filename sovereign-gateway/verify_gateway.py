import requests
import json

def test_gateway():
    base_url = "http://127.0.0.1:8000"
    
    print("Step 1: Testing Passport Issuance...")
    intent = "EXECUTE_SECURE_PAYMENT_v1"
    try:
        response = requests.post(f"{base_url}/issue-passport", json={"intent": intent}, timeout=5)
        if response.status_code != 200:
            print("FAIL: Could not issue passport.")
            return
        
        data = response.json()
        signature = data['signature']
        seed = data['seed']
        print(f"SUCCESS: Passport issued. Signature: {signature[:16]}...")
        
        print("\nStep 2: Testing Valid Verification...")
        verify_resp = requests.post(f"{base_url}/verify-passport", json={
            "intent": intent,
            "signature": signature,
            "seed": seed
        }, timeout=5)
        # Remove emojis to prevent Windows charmap encoding errors
        msg = verify_resp.json()['message'].replace('✅', '[SUCCESS]').replace('❌', '[DENIED]')
        print(f"Result: {msg}")
        assert verify_resp.json()['status'] == "VERIFIED"
        
        print("\nStep 3: Testing Tampered Verification (Red Team)...")
        tampered_intent = "EXECUTE_SECURE_PAYMENT_v2" 
        tampered_resp = requests.post(f"{base_url}/verify-passport", json={
            "intent": tampered_intent,
            "signature": signature,
            "seed": seed
        }, timeout=5)
        msg_tamper = tampered_resp.json()['message'].replace('✅', '[SUCCESS]').replace('❌', '[DENIED]')
        print(f"Result: {msg_tamper}")
        assert tampered_resp.json()['status'] == "REJECTED"
        
        print("\n--- ALL API GATEWAY TESTS PASSED ---")
    except requests.exceptions.ConnectionError:
        print("Error: Gateway server is not running on localhost:8000. Start main.py first.")

if __name__ == "__main__":
    test_gateway()
