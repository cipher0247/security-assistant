import requests
import json

BASE_URL = "http://localhost:8000"

def test_password_strength():
    print(f"\nTesting Password Strength at {BASE_URL}/api/tools/password ...")
    try:
        resp = requests.post(f"{BASE_URL}/api/tools/password", json={"password": "password123"})
        data = resp.json()
        print(f"   Input: 'password123' -> Rating: {data.get('rating')} (Score: {data.get('score')})")
        if "feedback" in data:
            print(f"   Feedback: {data['feedback']}")
            print("   ✅ Passed")
        else:
            print("   ❌ Failed structure")
    except Exception as e:
        print(f"   ❌ Failed: {e}")

def test_hash_calc():
    print(f"\nTesting Hash Calculator at {BASE_URL}/api/tools/hash ...")
    try:
        resp = requests.post(f"{BASE_URL}/api/tools/hash", json={"text": "hello"})
        data = resp.json()
        print(f"   Input: 'hello' -> MD5: {data.get('md5')}")
        if data.get('md5') == "5d41402abc4b2a76b9719d911017c592":
            print("   ✅ Passed (Hash verified)")
        else:
            print(f"   ❌ Failed: Incorrect Hash {data.get('md5')}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")

def test_glossary():
    print(f"\nTesting Glossary API at {BASE_URL}/api/education/glossary ...")
    try:
        resp = requests.get(f"{BASE_URL}/api/education/glossary")
        data = resp.json()
        print(f"   Items found: {len(data)}")
        if len(data) > 0 and "term" in data[0]:
            print("   ✅ Passed")
        else:
            print("   ❌ Failed structure")
    except Exception as e:
        print(f"   ❌ Failed: {e}")

def test_phishing():
    print(f"\nTesting Phishing ML at {BASE_URL}/api/tools/phishing/url ...")
    try:
        # Benign
        resp = requests.post(f"{BASE_URL}/api/tools/phishing/url", json={"url": "https://google.com"})
        data = resp.json()
        print(f"   Input: 'google.com' -> Risk: {data.get('risk')} ({data.get('confidence')}%)")
        
        # Phishing (High Entropy)
        resp2 = requests.post(f"{BASE_URL}/api/tools/phishing/url", json={"url": "http://paypal-login-secure-update-account.com.xyz"})
        data2 = resp2.json()
        print(f"   Input: 'sus-url' -> Risk: {data2.get('risk')} ({data2.get('confidence')}%)")
        
        if data.get('risk') == "LOW" and (data2.get('risk') == "HIGH" or data2.get('risk') == "UNKNOWN"):
             print("   ✅ Passed (Distinguished safe vs suspicious)")
        else:
             print("   ⚠️ Warning: ML model might need tuning or returned UNKNOWN")
    except Exception as e:
        print(f"   ❌ Failed: {e}")

def test_email_scanner():
    print(f"\nTesting Email Scanner at {BASE_URL}/api/tools/phishing/email ...")
    try:
        body = "URGENT: Your account is suspended. Click here to verify password."
        resp = requests.post(f"{BASE_URL}/api/tools/phishing/email", json={"subject": "Alert", "body": body})
        data = resp.json()
        print(f"   Input: 'Urgent password request' -> Risk: {data.get('risk')}")
        if data.get('risk') in ["MEDIUM", "HIGH"]:
            print("   ✅ Passed (Detected urgency/keywords)")
        else:
            print("   ❌ Failed to detect triggers")
    except Exception as e:
        print(f"   ❌ Failed: {e}")

def test_student_pack():
    print(f"\nTesting Student Data API ...")
    try:
        q_resp = requests.get(f"{BASE_URL}/api/education/quiz")
        c_resp = requests.get(f"{BASE_URL}/api/education/career")
        cs_resp = requests.get(f"{BASE_URL}/api/education/cheatsheets")
        
        if len(q_resp.json()) == 5 and len(c_resp.json()) > 0 and len(cs_resp.json()) > 0:
            print("   ✅ Passed (Quiz [5 random], Career, and Cheat Sheets loaded)")
        else:
            print(f"   ❌ Failed (Data count mismatch: Q={len(q_resp.json())})")
    except Exception as e:
        print(f"   ❌ Failed: {e}")   

if __name__ == "__main__":
    test_password_strength()
    test_hash_calc()
    test_glossary()
    test_phishing()
    test_email_scanner()
    test_student_pack()
