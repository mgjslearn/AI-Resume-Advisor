#!/usr/bin/env python3
"""
Test script for the Resume AI backend
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test if all required packages are available"""
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    print("✅ All packages imported successfully!")
    return True

if __name__ == "__main__":
    print("Testing Resume AI Backend Dependencies...")
    print("-" * 50)
    
    if test_imports():
        print("\n🎉 Backend is ready to run!")
        print("\nNext steps:")
        print("1. Get your Hugging Face API key from: https://huggingface.co/settings/tokens")
        print("2. Add it to backend/.env file")
        print("3. Run: conda activate resume-ai && python backend/main.py")
    else:
        print("\n❌ Some dependencies are missing. Please check your Python environment.")
