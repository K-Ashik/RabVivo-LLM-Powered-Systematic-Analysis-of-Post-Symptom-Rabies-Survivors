import streamlit as st
import sys

# Load secrets
groq_api_key = st.secrets["GROQ_API_KEY"]
print(f"✅ Groq API Key loaded: {groq_api_key[:10]}...")

# Test Groq connection
from groq import Groq

client = Groq(api_key=groq_api_key)

print("\n🔄 Testing Groq API connection with Llama 3.3 70B...")

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": "Say 'Hello from Groq and Llama 3.3!' in one sentence."
            }
        ],
        max_tokens=100
    )
    
    print("\n✅ Groq API Connection SUCCESS!")
    print(f"Model: llama-3.3-70b-versatile")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)