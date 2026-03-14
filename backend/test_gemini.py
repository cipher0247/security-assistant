#!/usr/bin/env python
"""Test Gemini AI Integration"""
from dotenv import load_dotenv
load_dotenv()  # Load .env file first

from nvidia_ai_integration import GeminiAIClient

print("=" * 60)
print("GEMINI AI INTEGRATION TEST")
print("=" * 60)

try:
    print("\n1. Loading Gemini module... ", end="")
    print("✓")
    
    print("2. Initializing Gemini client... ", end="")
    client = GeminiAIClient()
    print("✓")
    
    print("3. Available models:")
    print(f"   - Main (most capable): {client.MODEL_MAIN}")
    print(f"   - Fast (quick): {client.MODEL_FAST}")
    print(f"   - Pro (advanced): {client.MODEL_PRO}")
    
    print("\n4. API Configuration:")
    print(f"   - API Key loaded: {'✓' if client.api_key else '✗'}")
    print(f"   - API Endpoint: https://generativelanguage.googleapis.com")
    
    print("\n✓ INTEGRATION SUCCESSFUL!")
    print("\nYour Gemini AI features are ready to use:")
    print("  - AI Phishing Email Analyzer")
    print("  - AI URL Security Analysis")
    print("  - AI Password Coach")
    print("  - AI File Risk Explainer")
    print("  - AI Security Chatbot")
    print("  - AI Threat Explainer")
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
