import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-20b"

role = "user"
content = "How internet works explain in details"

message = {
    "role": role,
    "content": content    
}

messages = [message]

# response = client.chat.completions.create(model=model,messages=messages)
# print(response.choices[0].message.content)

stream = client.chat.completions.create(model=model,messages=messages, stream=True)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)