import requests
import json
import secrets
import hashlib

def get_quantum_entropy():
    try:
        response = requests.get("https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint16", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                return str(data['data'][0])
    except:
        pass
    return secrets.token_hex(16)

def generate_structural_signature(payload, q_seed):
    if isinstance(payload, (dict, list)):
        payload_str = json.dumps(payload, sort_keys=True)
    else:
        payload_str = str(payload)
    structure_base = f"{payload_str}|{q_seed}"
    sig_1 = hashlib.sha256(structure_base.encode()).hexdigest()
    final_signature = hashlib.sha256((sig_1 + structure_base).encode()).hexdigest()
    return final_signature

# Test
seed = get_quantum_entropy()
ai_intent = {"action": "EXECUTE_TRANSFER_ACTION_001", "clearance": "Sovereign_Level_4"}
passport_sig = generate_structural_signature(ai_intent, seed)

# Scenarios
assert passport_sig == generate_structural_signature(ai_intent, seed)
tampered_intent = ai_intent.copy()
tampered_intent["action"] = "EXECUTE_TRANSFER_ACTION_999"
assert passport_sig != generate_structural_signature(tampered_intent, seed)

print("Verification SUCCESS: Aligned logic gates passed.")
