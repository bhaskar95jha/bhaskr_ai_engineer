import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API key kaha hai bhai")

client = Groq(api_key=api_key)
model = "openai/gpt-oss-20b"

JD = """
Job Title: Backend Java Developer

Experience: 3–5 Years

Job Description:

We are looking for a Backend Java Developer to design, develop, and maintain scalable backend services and APIs. The candidate should have strong experience in Java, Spring Boot, REST APIs, microservices, databases, cloud technologies, and containerized applications.

Responsibilities:

* Develop scalable backend applications using Java and Spring Boot.
* Design and develop REST APIs and microservices.
* Work with PostgreSQL or other relational databases.
* Implement business logic, data processing, and service integrations.
* Develop and maintain unit and integration tests.
* Troubleshoot production issues and improve application performance.
* Build and deploy applications using Docker and Kubernetes.
* Work with AWS services such as S3, Glue, Athena, IAM, and CloudWatch.
* Work with asynchronous workflows and distributed systems.
* Participate in code reviews, debugging, and technical design discussions.

Required Skills:

* Java 17+
* Spring Boot
* Spring Data JPA / Hibernate
* REST APIs
* Microservices
* PostgreSQL / SQL
* Maven
* JUnit / Mockito
* Git
* Docker
* Kubernetes
* AWS
* Data structures and algorithms
* Basic system design

Good to Have:

* gRPC and Protocol Buffers
* Apache Kafka
* AWS Glue / Athena
* Apache Iceberg
* Argo Workflows
* Python / PySpark
* CI/CD
* Terraform

Project Experience:

The candidate should have experience building backend services or data-processing systems involving multiple APIs and external services. Experience with cloud-based ETL pipelines, workflow orchestration, containerized deployments, or distributed systems is preferred.

Interview Focus:

* Core Java and OOP
* Collections, Streams, Exception Handling, Multithreading
* Spring Boot and dependency injection
* REST API design
* Database and SQL concepts
* Microservices and system design
* Docker and Kubernetes
* AWS fundamentals
* DSA and problem solving
* Debugging and production troubleshooting
"""

RESUME = """
# Rahul Sharma

Email: [rahul.sharma@example.com](mailto:rahul.sharma@example.com)
Phone: +91-9876543210
Location: Bengaluru, India
LinkedIn: linkedin.com/in/rahulsharma
GitHub: github.com/rahulsharma

## PROFESSIONAL SUMMARY

Backend Java Developer with 4 years of experience building scalable backend applications and REST APIs using Java 17, Spring Boot, Spring Data JPA, and microservices. Experienced in PostgreSQL, AWS, Docker, Kubernetes, unit testing, and distributed systems. Strong understanding of API design, cloud deployments, debugging, performance optimization, and data structures and algorithms.

## TECHNICAL SKILLS

**Languages:** Java 17, SQL, Python

**Backend:** Spring Boot, Spring Data JPA, Hibernate, REST APIs, Microservices

**Databases:** PostgreSQL, MySQL

**Testing:** JUnit, Mockito, Integration Testing

**Cloud:** AWS S3, AWS Glue, AWS Athena, AWS IAM, AWS CloudWatch

**DevOps:** Docker, Kubernetes, Git, Maven, CI/CD

**Architecture:** Microservices, Distributed Systems, System Design

**Additional:** gRPC, Protocol Buffers, Apache Kafka, Argo Workflows, Apache Iceberg, PySpark

**Core Concepts:** OOP, Collections, Streams, Exception Handling, Multithreading, Data Structures and Algorithms

## PROFESSIONAL EXPERIENCE

### Senior Software Engineer — ABC Technologies

Bengaluru, India
2022 – Present

* Developed scalable backend microservices using **Java 17, Spring Boot, Spring Data JPA, and Hibernate**.
* Designed and implemented **REST APIs** for data processing, workflow management, and service integrations.
* Built backend services integrating with **AWS S3, Glue, Athena, IAM, and CloudWatch**.
* Developed **gRPC APIs and clients using Protocol Buffers** for communication between distributed services.
* Created containerized applications using **Docker** and deployed services on **Kubernetes**.
* Worked with PostgreSQL databases and optimized SQL queries for improved application performance.
* Implemented unit and integration tests using **JUnit and Mockito**.
* Participated in code reviews, technical design discussions, debugging, and production issue resolution.
* Improved backend performance by optimizing database queries, API calls, and service communication.
* Worked with asynchronous workflows using **Argo Workflows**.
* Implemented data-processing pipelines using **AWS Glue, PySpark, and Apache Iceberg**.
* Used Git and Maven for source control and build management.
* Worked with **Apache Kafka** for event-driven communication between services.
* Investigated production failures using application logs and **AWS CloudWatch**.
* Followed microservice and distributed-system design principles for scalable applications.

### Software Engineer — XYZ Solutions

Pune, India
2020 – 2022

* Developed RESTful backend services using **Java and Spring Boot**.
* Implemented business logic using OOP principles, Java Collections, Streams, and Exception Handling.
* Developed database integrations using **Spring Data JPA and Hibernate**.
* Designed SQL queries and worked with **PostgreSQL**.
* Created automated tests using **JUnit and Mockito**.
* Dockerized Java applications and supported deployments on Kubernetes environments.
* Fixed production issues related to API failures, database errors, and application performance.
* Used Git and Maven for version control and application builds.
* Participated in system design and code review activities.

## PROJECTS

### Cloud-Based Data Processing Platform

**Technologies:** Java 17, Spring Boot, AWS S3, AWS Glue, AWS Athena, PostgreSQL, Docker, Kubernetes, Argo Workflows, Apache Iceberg

* Developed Spring Boot microservices to manage cloud-based data processing workflows.
* Built REST and gRPC APIs for triggering and monitoring data-processing jobs.
* Integrated AWS Glue and Athena for ETL processing and analytical workloads.
* Stored processed data using Apache Iceberg on Amazon S3.
* Deployed backend services using Docker and Kubernetes.
* Used Argo Workflows for workflow orchestration.
* Implemented logging and monitoring using AWS CloudWatch.

### Event-Driven Order Processing System

**Technologies:** Java 17, Spring Boot, Kafka, PostgreSQL, Docker, Kubernetes

* Developed microservices for order creation, payment processing, and notification handling.
* Used Apache Kafka for asynchronous communication between services.
* Implemented REST APIs and PostgreSQL persistence using Spring Data JPA.
* Added unit and integration tests using JUnit and Mockito.
* Containerized services using Docker and deployed them on Kubernetes.

## EDUCATION

Bachelor of Technology in Computer Science
ABC University, India
2020

## KEY STRENGTHS

* Backend Development
* Microservices
* REST API Design
* Cloud Integration
* Distributed Systems
* Database Design
* Debugging & Troubleshooting
* System Design
* Data Structures & Algorithms
* Test Automation
"""

def ask_llm(system_prompt, user_prompt):
    sys_msg={
        "role": "system",
        "content": system_prompt
    }
    user_msg={
        "role": "user",
        "content": user_prompt
    }

    messages = [sys_msg, user_msg]

    response = client.chat.completions.create(
        model=model,messages=messages,temperature=0
    )
    answer = response.choices[0].message.content
    return answer

def step1_res_extract(RESUME):
    print("STEP 1")
    system_prompt="""
    You are a professional HR assistant. Extract the skills from the candidates resume provided.
    Only return the skills no other information. Do not invent any skillsby yourself.
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
    Extract the skills from this resume
    {RESUME}
    """
    return ask_llm(system_prompt, user_prompt)

def step2_JD_extract(JD):
    print("step2")
    system_prompt="""
    You are a professional HR assistant. Extract the skills from the Job description  provided.
    Only return the skills no other information. Do not invent any skills by yourself.
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
    Extract the skills from this JD
    {JD}
    """
    return ask_llm(system_prompt, user_prompt)

def step3_match(candidate,jd):
    print("step3")
    system_prompt="""
    You are a professional HR assistant. compare the skills of candidate and the skills required in the JD and produce a final score between
    1 and 100. also produce a short verdict whther the candidate is a good fit for the role.
    """
    user_prompt=f"""
    Compare and match the skills
    JD:
    {jd}
    Candidate:
    {candidate}
    """
    return ask_llm(system_prompt, user_prompt)

candidate=step1_res_extract(RESUME)
print(candidate)
sleep(2)
jd=step2_JD_extract(JD)
print(jd)
sleep(2)
score=step3_match(candidate,jd)
print(score)