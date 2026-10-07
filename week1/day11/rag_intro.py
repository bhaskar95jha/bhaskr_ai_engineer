import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=api_key)
model = "openai/gpt-oss-20b"

# step:1 knowledge base
knowledge_base = {
    "bhaskar jha": {
        "age": 30,
        "company": "Candescent",
        "previous_company": "Fico",
        "education": "NIT Raipur"
    }
}

# step 2
def retrieve_from_knowledge_base(query):
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value
    return None

def ask_llm(question):
    context = retrieve_from_knowledge_base(question)
    sys_prompt = f"""answer in one line and give the answer in a very simple way and Answer only based on the context provided : {context}"""
    system_message = {
        "role": "system",
        "content": sys_prompt
    }

    message = {
        "role": "user",
        "content": question
    }

    messages = [system_message, message]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content

question = "where bhaskar jha complete his education?"
print(ask_llm(question))