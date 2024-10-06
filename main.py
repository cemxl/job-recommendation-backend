from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define FastAPI app
app = FastAPI()

# Database connection setup
DATABASE_URL = "postgresql://postgres:cemal%402003@localhost/job_recommendation_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Job Posting model (SQLAlchemy schema for PostgreSQL)
class JobPostingDB(Base):
    __tablename__ = "job_postings"
    job_id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, index=True)
    company = Column(String)
    required_skills = Column(ARRAY(String))
    location = Column(String)
    job_type = Column(String)
    experience_level = Column(String)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Define the Preferences schema for API
class Preferences(BaseModel):
    desired_roles: List[str]
    locations: List[str]
    job_type: List[str]

# Update the UserProfile schema for API
class UserProfile(BaseModel):
    name: str
    skills: List[str]
    experience_level: str
    preferences: Preferences

# Define the Job Posting schema for API
class JobPosting(BaseModel):
    job_id: int
    job_title: str
    company: str
    required_skills: List[str]
    location: str
    job_type: str
    experience_level: str

@app.get("/")
async def welcome():
    return {"message": "Welcome to the Job Recommendation API!"}

@app.post("/add_job")
async def add_job(job_posting: JobPosting):
    db = SessionLocal()
    db_job = JobPostingDB(
        job_id=job_posting.job_id,
        job_title=job_posting.job_title,
        company=job_posting.company,
        required_skills=job_posting.required_skills,
        location=job_posting.location,
        job_type=job_posting.job_type,
        experience_level=job_posting.experience_level
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    db.close()
    return {"message": "Job added successfully!", "job_id": db_job.job_id}

@app.post("/recommend")
async def recommend_jobs(user_profile: UserProfile):
    db = SessionLocal()
    
    # Mock data for job postings (You can also retrieve this from the database)
    mock_jobs = [
        JobPostingDB(
            job_id=1,
            job_title="Software Engineer",
            company="Tech Solutions Inc.",
            required_skills=["JavaScript", "React", "Node.js"],
            location="San Francisco",
            job_type="Full-Time",
            experience_level="Intermediate"
        ),
        JobPostingDB(
            job_id=2,
            job_title="Data Scientist",
            company="Data Analytics Corp.",
            required_skills=["Python", "Data Analysis", "Machine Learning"],
            location="Remote",
            job_type="Full-Time",
            experience_level="Intermediate"
        ),
        JobPostingDB(
            job_id=3,
            job_title="Frontend Developer",
            company="Creative Designs LLC",
            required_skills=["HTML", "CSS", "JavaScript", "Vue.js"],
            location="New York",
            job_type="Part-Time",
            experience_level="Junior"
        ),
        JobPostingDB(
            job_id=4,
            job_title="Backend Developer",
            company="Web Services Co.",
            required_skills=["Python", "Django", "REST APIs"],
            location="Chicago",
            job_type="Full-Time",
            experience_level="Senior"
        ),
        JobPostingDB(
            job_id=5,
            job_title="Machine Learning Engineer",
            company="AI Innovations",
            required_skills=["Python", "Machine Learning", "TensorFlow"],
            location="Boston",
            job_type="Full-Time",
            experience_level="Intermediate"
        ),
        JobPostingDB(
            job_id=6,
            job_title="DevOps Engineer",
            company="Cloud Networks",
            required_skills=["AWS", "Docker", "Kubernetes"],
            location="Seattle",
            job_type="Full-Time",
            experience_level="Senior"
        ),
        JobPostingDB(
            job_id=7,
            job_title="Full Stack Developer",
            company="Startup Hub",
            required_skills=["JavaScript", "Node.js", "Angular", "MongoDB"],
            location="Austin",
            job_type="Full-Time",
            experience_level="Intermediate"
        ),
        JobPostingDB(
            job_id=8,
            job_title="Data Analyst",
            company="Finance Analytics",
            required_skills=["SQL", "Python", "Tableau"],
            location="New York",
            job_type="Full-Time",
            experience_level="Junior"
        ),
        JobPostingDB(
            job_id=9,
            job_title="Quality Assurance Engineer",
            company="Reliable Software",
            required_skills=["Selenium", "Java", "Testing"],
            location="San Francisco",
            job_type="Contract",
            experience_level="Intermediate"
        ),
        JobPostingDB(
            job_id=10,
            job_title="Systems Administrator",
            company="Enterprise Solutions",
            required_skills=["Linux", "Networking", "Shell Scripting"],
            location="Remote",
            job_type="Full-Time",
            experience_level="Senior"
        )
    ]

    recommended_jobs = []

    # Match user profile with job postings
    for job in mock_jobs:
        score = 0
        
        # Strict match for job title
        if job.job_title in user_profile.preferences.desired_roles:
            score += 2  # Higher score for exact match
        
        # Strict match for location
        if job.location in user_profile.preferences.locations:
            score += 2  # Higher score for exact match
            
        # Check for partial skill match
        skills_match_count = len(set(user_profile.skills) & set(job.required_skills))
        if skills_match_count > 0:
            score += 1  # One point for any skill match
            if skills_match_count >= 2:
                score += 1  # Bonus point for two or more skill matches
        
        # Check job type match
        if job.job_type in user_profile.preferences.job_type:
            score += 1
            
        # Check experience level match
        if job.experience_level == user_profile.experience_level:
            score += 1

        # Set a threshold for recommending a job
        if score >= 4:  # Adjust the threshold based on your preference
            recommended_jobs.append(job)

    db.close()

    return {
        "recommended_jobs": [
            {
                "job_title": job.job_title,
                "company": job.company,
                "location": job.location,
                "job_type": job.job_type,
                "required_skills": job.required_skills,
                "experience_level": job.experience_level
            }
            for job in recommended_jobs
        ]
    }
