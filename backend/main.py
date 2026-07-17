from graph import graph
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session
import os

import models
import schemas
from database import engine, get_db
from auth import hash_password, verify_password, create_access_token, get_current_student

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