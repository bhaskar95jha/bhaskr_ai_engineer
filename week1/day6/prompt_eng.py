import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=api_key)
# models = client.models.list()
# print("Available models:")
# for model in models:
#     print(model.id)
# print("+++++++++++++++++++++++++++++++++++++++++++++++++++\n")    
model = "openai/gpt-oss-20b"

def llm_ans(prompt):
    role = "user"
    content = prompt

    message = {
        "role": role,
        "content": content
    }

    messages = [message]

    response = client.chat.completions.create(model=model, messages=messages)

    return response.choices[0].message.content

prompt = """
#ROLE:
You are a support assistant at a mobile/laptop company.
#TASK:
You have to classify the issue in a category.
#CONSTRAINT:
You have to classify the issue in one of three categories namely billing, technical, return
#OUTPUT FORMAT:
Your answer should be in one word and should be one of the three categories mentioned above.
#Example:
For instance, if the user says "I have a problem with my bill", you should respond with "billing".
#FALLBACK:
If the issue does not fall into any of the three categories, respond with "OTHERS".
This is a User Complaint.
My laptop is not turning on even after charging it for 2 hours.i want refund my money back.
"""

print(llm_ans(prompt))