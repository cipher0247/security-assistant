import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.utils.tools_extended import SteganographyTool, PasswordGenerator, ExifViewer, NewsFetcher
from PIL import Image
import io

def test_password_generator():
    print("Testing Password Generator...")
    pwd = PasswordGenerator.generate(length=12, use_symbols=True)
    assert len(pwd) == 12
    assert any(c in "!@#$%^&*()-_=+" for c in pwd)
    print(f"✅ Password Gen Passed: {pwd}")

def test_password_strength_advanced():
    print("Testing Password Strength Advanced Scenarios...")
    from backend.scanners.password_strength import PasswordStrengthChecker
    checker = PasswordStrengthChecker()
    
    # Test 1: Online Attack (Should be very slow/year)
    res_online = checker.check_strength("password123", attack_mode='online')
    print(f"   Online Mode: {res_online['crack_time_estimate']} (Rate: {res_online['guesses_per_second']}/s)")
    assert res_online['guesses_per_second'] == 100
    
    # Test 2: Offline GPU MD5 (Should be instant)
    res_gpu_md5 = checker.check_strength("abc1", attack_mode='offline', hardware='gpu', hash_type='md5')
    print(f"   Offline GPU MD5: {res_gpu_md5['crack_time_estimate']} (Rate: {res_gpu_md5['guesses_per_second']}/s)")
    assert res_gpu_md5['crack_time_estimate'] == 'Instantly'
    
    # Test 3: Offline CPU Bcrypt (Should be slower)
    res_cpu_bcrypt = checker.check_strength("password123", attack_mode='offline', hardware='cpu', hash_type='bcrypt')
    print(f"   Offline CPU Bcrypt: {res_cpu_bcrypt['crack_time_estimate']} (Rate: {res_cpu_bcrypt['guesses_per_second']}/s)")
    assert res_cpu_bcrypt['guesses_per_second'] == 50
    
    print("✅ Advanced Strength Scenarios Passed")

def test_steganography():
    print("\nTesting Steganography...")
    # Create white image
    img = Image.new('RGB', (100, 100), color='white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    original_bytes = img_byte_arr.getvalue()
    
    secret = "CyberSecurityRules!"
    encoded_bytes = SteganographyTool.hide_text(original_bytes, secret)
    decoded_text = SteganographyTool.extract_text(encoded_bytes)
    
    if secret != decoded_text:
        print(f"❌ Stego Failed! Expected: '{secret}' Got: '{decoded_text}' Len: {len(decoded_text)}")
    assert secret == decoded_text
    print(f"✅ Steganography Passed: {decoded_text}")

def test_exif():
    print("\nTesting Exif...")
    # Create image with simple data (Pillow limitations on writing exif easily without loading)
    # So we just test the viewer handles no-exif gracefully
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    
    metadata = ExifViewer.get_metadata(img_byte_arr.getvalue())
    assert isinstance(metadata, dict)
    print("✅ Exif Viewer Passed (Basic)")

def test_news_fetcher():
    print("\nTesting News Fetcher...")
    news = NewsFetcher.get_latest_news(limit=3)
    # Might fail if no internet, but logic check
    if news:
        assert 'title' in news[0]
        print(f"✅ News Fetcher Passed: Found {len(news)} articles")
    else:
        print("⚠️ News Fetcher: No internet or feed error (Expected in some envs)")

if __name__ == "__main__":
    try:
        test_password_generator()
        test_password_strength_advanced()
        test_steganography()
        test_exif()
        test_news_fetcher()
        print("\nAll System Checks Passed!")
    except Exception as e:
        print(f"\n❌ Verification Failed: {e}")
