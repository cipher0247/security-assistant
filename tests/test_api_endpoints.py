import requests
import io

BASE_URL = "http://localhost:8000"

def test_health():
    print(f"Checking Health at {BASE_URL}/health ...")
    try:
        resp = requests.get(f"{BASE_URL}/health")
        if resp.status_code == 200:
            print(f"✅ Health Check Passed: {resp.json()}")
        else:
            print(f"❌ Health Check Failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

def test_file_scan():
    print(f"\nTesting File Scan at {BASE_URL}/api/scan/file ...")
    
    # 1. Test Benign File
    files = {'file': ('safe.txt', io.BytesIO(b"This is a safe text file."), 'text/plain')}
    try:
        resp = requests.post(f"{BASE_URL}/api/scan/file", files=files)
        data = resp.json()
        print(f"   Scan benign file: Risk={data.get('risk_level')} (Expected: LOW)")
        if data.get('risk_level') == 'LOW':
            print("   ✅ Passed")
        else:
            print(f"   ❌ Failed: Got {data.get('risk_level')}")
    except Exception as e:
        print(f"   ❌ Request Failed: {e}")

    # 2. Test Suspicious File (Mocking a binary with high entropy)
    import os
    random_content = os.urandom(1024) # High entropy
    files = {'file': ('malware.exe', io.BytesIO(random_content), 'application/octet-stream')}
    try:
        resp = requests.post(f"{BASE_URL}/api/scan/file", files=files)
        data = resp.json()
        print(f"   Scan suspicious file: Risk={data.get('risk_level')} (Expected: HIGH/MEDIUM)")
        if data.get('risk_level') in ['HIGH', 'MEDIUM']:
            print("   ✅ Passed")
        else:
            print(f"   ❌ Failed: Got {data.get('risk_level')}")
    except Exception as e:
        print(f"   ❌ Request Failed: {e}")

def test_url_scan():
    print(f"\nTesting URL Scan at {BASE_URL}/api/scan/url ...")
    
    # Test example.com
    payload = {"url": "https://example.com"}
    try:
        resp = requests.post(f"{BASE_URL}/api/scan/url", json=payload)
        data = resp.json()
        print(f"   Scan example.com: Risk={data.get('risk_level')}")
        # We don't assert exact risk here as it depends on live site headers, but we expect a result.
        if "risk_level" in data:
            print(f"   ✅ Passed (Status: {data.get('status_code')})")
        else:
            print(f"   ❌ Failed: Invalid response structure")
    except Exception as e:
        print(f"   ❌ Request Failed: {e}")

def test_frontend_availability():
    print(f"\nTesting Frontend Availability at {BASE_URL}/app/index.html ...")
    try:
        resp = requests.get(f"{BASE_URL}/app/index.html")
        if resp.status_code == 200 and "<title>Security Assistant</title>" in resp.text:
             print(f"   ✅ Passed (UI Loaded, Security Assistant title found)")
        else:
             print(f"   ❌ Failed: Status {resp.status_code} or title missing")
    except Exception as e:
        print(f"   ❌ Failed to load frontend: {e}")

if __name__ == "__main__":
    test_health()
    test_frontend_availability() # Added frontend check
    test_file_scan()
    test_url_scan()
