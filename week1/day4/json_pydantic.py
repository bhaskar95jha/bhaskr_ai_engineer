import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=api_key)

# Structure the output in a JSON format with the following fields: name, email, phone_number, and issue_description. The values for these fields should be extracted from the user's message. If any of the fields are not present in the message, they should be set to null.
from pydantic import BaseModel
class UserInfo(BaseModel):
    name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    issue_description: str | None = None

schema = UserInfo.model_json_schema()

response_format={
    "type": "json_object",
}

system_content = f"""
Extract the personal information from the UserInfo Strictly based on this schema {schema}. The output should be in JSON format and should include the following fields: name, email, phone_number, and issue_description. If any of the fields are not present in the user's message, they should be set to null.
"""
role = "system"
sys_message = {
    "role": role,
    "content": system_content
}

role = "user"
text = "Hello my name is bhaskar. I have purchased a car from a dealer and its not working properly. I want to return the car and get my money back. Can you help me with that? my email address is bhaskar@example.com and my phone number is 123-456-7890. I would like to know the process for returning the car and getting a refund. Please provide me with the necessary steps and any required documentation."

content = f"""
You are a helpful assistant. Please extract the personal information from the user's message: {text}"""

message = {
    "role": role,
    "content": content
}

messages = [sys_message, message]
model = "openai/gpt-oss-20b"

response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
ans = response.choices[0].message.content
print(ans)


# how to read this Json
import json
row_json = ans
data_file = json.loads(row_json)
user_info = UserInfo(**data_file)
print(user_info.name)
print(user_info.email)
print(user_info.phone_number)
print(user_info.issue_description)

