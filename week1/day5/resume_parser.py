import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader

def calculate_match(candidate, job_requirement):

    EXPERIENCE_WEIGHT = 20
    SKILL_WEIGHT = 50
    PROJECT_WEIGHT = 30

    # Experience
    if candidate.experience_years >= job_requirement.experience_years:
        experience_score = EXPERIENCE_WEIGHT
    else:
        experience_score = 0

    # Skills
    candidate_skills = set(skill.lower() for skill in candidate.skill)
    required_skills = set(skill.lower() for skill in job_requirement.skill)

    matched_skills = candidate_skills.intersection(required_skills)

    skill_percentage = (
        len(matched_skills) / len(required_skills) * 100
        if required_skills
        else 0
    )

    skill_score = skill_percentage * SKILL_WEIGHT / 100

    # Projects
    candidate_projects = set(
        project.lower() for project in candidate.projects
    )

    required_projects = set(
        project.lower() for project in job_requirement.projects
    )

    matched_projects = candidate_projects.intersection(required_projects)

    project_percentage = (
        len(matched_projects) / len(required_projects) * 100
        if required_projects
        else 0
    )

    project_score = project_percentage * PROJECT_WEIGHT / 100

    # Final score
    final_score = (
        experience_score
        + skill_score
        + project_score
    )

    decision = "Selected" if final_score >= 80 else "Rejected"

    return {
        "experience_score": experience_score,
        "skill_score": skill_score,
        "project_score": project_score,
        "matched_skills": list(matched_skills),
        "matched_projects": list(matched_projects),
        "final_score": round(final_score, 2),
        "decision": decision
    }

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=api_key)

from pydantic import BaseModel, Field
class CandidateSkill(BaseModel):
    experience_years: float | None = None
    skill: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)

schema = CandidateSkill.model_json_schema()

response_format={
    "type": "json_object",
}

system_content = f"""
Extract the experience, skills, and projects from the CandidateSkill Strictly based on this schema {schema}. The output should be in JSON format and should include the following fields: experience_years, skill, and projects. If any of the fields are not present in the user's message, they should be set to null.
"""
role = "system"
sys_message = {
    "role": role,
    "content": system_content
}


role = "user"
file_path = Path("resources/resume.pdf")
reader = PdfReader(file_path)
resume_text = ""
for page in reader.pages:
    resume_text += page.extract_text() or ""

content = f"""
You are a helpful assistant. Calculate the candidate's total professional full-time experience from the employment dates provided in the resume. Do not rely on experience claims mentioned in the resume summary. Exclude internships. Return the total experience as a whole number of years. , skill and projects from the following resume text: {resume_text}"""

message = {
    "role": role,
    "content": content
}

messages = [sys_message, message]
model = "openai/gpt-oss-20b"

response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
ans = response.choices[0].message.content
print(ans)

class JobRequirements(BaseModel):
    experience_years: float | None = None
    skill: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)

schema = JobRequirements.model_json_schema()

text = f"""We are looking for a Backend Java Developer.

Experience:
Minimum 4 years

Required Skills:
Java
Spring Boot
AWS
Docker
Kubernetes

Required Project Experience:
Enterprise Content Management systems
Social Media Data Extraction or Social Media Integration
Visual Studio Extensions or Developer Tools"""

jd_content = f"""You are a helpful assistant. Extract the experience, skills, and projects from the JobRequirements Strictly based on this schema {schema}. The output should be in JSON format and should include the following fields: experience_years, skill, and projects. If any of the fields are not present in the job description, they should be set to null. The job description is as follows: {text}"""

jd_message = {
    "role": role,
    "content": jd_content
}
print("###############################################################")
jd_messages = [sys_message, jd_message]
jd_response = client.chat.completions.create(model=model, messages=jd_messages, response_format=response_format)
jd_ans = jd_response.choices[0].message.content
print(jd_ans)

# # how to read this Json
import json
row_json = ans
data_file = json.loads(row_json)
cand_skill = CandidateSkill(**data_file)
row_json = jd_ans
data_file = json.loads(row_json)
job_req = JobRequirements(**data_file)

result = calculate_match(cand_skill, job_req)
print(result)


