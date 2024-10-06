# Job Recommendation Backend Service

## Description
This project implements a backend service that recommends relevant job postings based on user profiles and preferences using FastAPI and PostgreSQL.

## Features
- RESTful API for job recommendations
- Ability to add job postings
- Customizable recommendation logic

## Technologies Used
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

## Setup Instructions
1. Clone the repository: `git clone https://github.com/cemxl/job-recommendation-backend.git`
2. Navigate to the project directory: `cd job-recommendation-backend`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up your PostgreSQL database.
5. Run the application: `uvicorn main:app --reload`

## API Endpoints
- `POST /add_job`: Add a new job posting.
- `POST /recommend`: Get job recommendations based on user profile.

## Example Usage
To add a job posting:

{
  "job_id": 1,
  "job_title": "Software Engineer",
  "company": "Tech Solutions Inc.",
  "required_skills": ["Python", "Django"],
  "location": "Remote",
  "job_type": "Full-Time",
  "experience_level": "Intermediate"
}

To get job recommendations:

{
  "name": "Jane Doe",
  "skills": ["Python", "Django"],
  "experience_level": "Intermediate",
  "preferences": {
    "desired_roles": ["Software Engineer"],
    "locations": ["Remote"],
    "job_type": ["Full-Time"]
  }
}

## Contribution
Contributions are welcome! Please open an issue or submit a pull request.

## License
MIT License
