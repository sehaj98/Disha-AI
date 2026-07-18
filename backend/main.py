from datetime import date, datetime

from graph import graph
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
import os

import models
import schemas
from database import engine, get_db
from auth import hash_password, verify_password, create_access_token, get_current_student
from services.updates_service import get_updates_for_student
from services.email_service import send_update_email
from scheduler import send_due_updates

# Load .env file
load_dotenv()

# Read API Key
API_KEY = os.getenv("GEMINI_API_KEY")

print("API Key Loaded:", API_KEY is not None)
print("API Key:", API_KEY[:10] + "..." if API_KEY else "NOT FOUND")


# Create Gemini Client
client = genai.Client(api_key=API_KEY)

# Create the students table if it doesn't exist yet (disha.db, a local SQLite file)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Disha AI",
    description="Student Growth & Guidance Agent",
    version="1.0"
)

# Allow the Vite dev server (and any local frontend) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Background scheduler: checks once a day which students are due for an
# email (see scheduler.py / EMAIL_INTERVAL_DAYS in .env). next_run_time
# makes it also run once immediately on startup so you can see it work
# without waiting a full day during development.
scheduler = BackgroundScheduler()
scheduler.add_job(send_due_updates, "interval", hours=24, next_run_time=datetime.now())
scheduler.start()

# Request model
class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Welcome to Disha AI Backend!"}


@app.post("/signup", response_model=schemas.TokenResponse)
def signup(payload: schemas.SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(models.Student).filter(models.Student.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    student = models.Student(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        current_class=payload.current_class,
        country=payload.country,
        interests=payload.interests or [],
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    token = create_access_token({"sub": student.email})
    return {"access_token": token}


@app.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.email == payload.email).first()
    if not student or not verify_password(payload.password, student.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")

    token = create_access_token({"sub": student.email})
    return {"access_token": token}


@app.get("/me", response_model=schemas.StudentProfile)
def me(current_student: models.Student = Depends(get_current_student)):
    return current_student


@app.get("/updates")
def updates(current_student: models.Student = Depends(get_current_student)):
    """Logged-in students get a live, class-aware digest without asking
    a question first."""
    digest = get_updates_for_student(current_student)
    return {"digest": digest}


@app.post("/updates/send-now")
def send_now(
    current_student: models.Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """Manual trigger for testing: emails the logged-in student their
    digest immediately, bypassing the schedule's due-date check."""
    digest = get_updates_for_student(current_student)
    sent = send_update_email(current_student.email, current_student.name, digest)

    if sent:
        current_student.last_emailed_at = date.today()
        db.add(current_student)
        db.commit()

    return {"sent": sent}


@app.post("/chat")
def chat(request: ChatRequest):

    state = {
        "messages": [request.message],
        "status": "",
        "student_class": "",
        "country": "",
        "interests": [],
        "stream": "",
        "response": ""
    }

    result = graph.invoke(state)

    return {
        "response": result["response"]
    }
    