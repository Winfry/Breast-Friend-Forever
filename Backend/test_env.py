# test_env.py
import os
from dotenv import load_dotenv

print("🔍 Testing .env file...")
print("=" * 40)

# Load environment variables
load_dotenv()

# Check if key exists
api_key = os.getenv('OPENAI_API_KEY')

if api_key:
    print(f"✅ OPENAI_API_KEY: FOUND ({api_key[:20]}...)")
else:
    print("❌ OPENAI_API_KEY: MISSING - Please add it to .env file")

# Check other important variables
if os.getenv('SECRET_KEY'):
    print("✅ SECRET_KEY: FOUND")
else:
    print("❌ SECRET_KEY: MISSING")

print("=" * 40)

if api_key:
    print("🎉 Your .env file looks good!")
    print("🚀 Now let's test the server...")
else:
    print("⚠️  Please fix your .env file first")