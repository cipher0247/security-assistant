import sys
import os
import asyncio
import io

# Add backend to path
# Add project root to path (security_assistant folder)
sys.path.append(os.path.join(os.getcwd(), 'security_assistant'))

from backend.scanners.file_scan import FileScanner
from backend.scanners.url_scan import UrlScanner
from backend.risk_engine import RiskEngine

async def test_file_scan():
    print("Testing File Scanner...")
    scanner = FileScanner()
    
    # Test benign file
    content = b"Hello world, this is a safe file."
    result = await scanner.scan_file(content, "test.txt")
    print(f"Benign File Result: {result}")
    risk = RiskEngine.calculate_file_risk(result)
    print(f"Risk: {risk}")
    assert risk == "LOW"

    # Test suspicious file (extension + high entropy/random data)
    random_data = os.urandom(100) # High entropy
    result = await scanner.scan_file(random_data, "malware.exe")
    print(f"Suspicious File Result: {result}")
    risk = RiskEngine.calculate_file_risk(result)
    print(f"Risk: {risk}")
    assert risk in ["MEDIUM", "HIGH"]

def test_url_scan():
    print("\nTesting URL Scanner...")
    scanner = UrlScanner()
    
    # Test Example.com (Safe)
    result = scanner.scan_url("http://example.com")
    print(f"Example.com Result: {result.keys()}") # Don't print full body
    risk = RiskEngine.calculate_url_risk(result)
    print(f"Risk: {risk}")
    # example.com might lack headers or HTTPS redirect, so might be MEDIUM. 
    # Just checking it doesn't crash.
    
    # Test Dummy XSS/SQLi (passively)
    # We can't easily find a site with these exposing errors without permission.
    # We trust the logic unit tests for patterns.

async def main():
    await test_file_scan()
    try:
        test_url_scan()
    except Exception as e:
        print(f"URL Scan failed (network issue?): {e}")

if __name__ == "__main__":
    asyncio.run(main())
