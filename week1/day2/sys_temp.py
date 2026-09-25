import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=api_key)

role = "system"
content = "You are a pediatrician. You are an expert in child health and development. You provide accurate and helpful advice to parents regarding their children's health, growth, and well-being."

sys_message = {
    "role": role,
    "content": content
}

role = "user"
content = "what about for 21 moths girls baby?"

message = {
    "role": role,
    "content": content
}

messages = [sys_message, message]
model = "openai/gpt-oss-20b"

response = client.chat.completions.create(model=model, messages=messages, temperature=0.5)

print(response.choices[0].message.content)