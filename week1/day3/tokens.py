import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=api_key)

role = "user"
model = "openai/gpt-oss-20b"

prompt1 = "Hi"
prompt2 = "Explain why Ai engineering is good for carrer growth"
prompt3 = "Explain Diff between ML engineer and AI engineer in 100 words"

prompts = [prompt1, prompt2, prompt3]
for content in prompts:
    message = {
        "role": role,
        "content": content
    }
    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages, max_tokens=10000)
    usage = response.usage
    print(f"Prompt: {content}")
    print(f"your token: {usage.prompt_tokens}")
    print(f"completion token: {usage.completion_tokens}")
    print(f"Tokens used: {usage.total_tokens}")
    print(f"Finish reason: {response.choices[0].finish_reason}")

# content = "what about for 21 moths girls baby?"

# message = {
#     "role": role,
#     "content": content
# }

# messages = [sys_message, message]
#

# response = client.chat.completions.create(model=model, messages=messages, temperature=0.5)

# print(response.choices[0].message.content)