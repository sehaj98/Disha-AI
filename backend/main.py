from graph import graph
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os

# Load .env file
load_dotenv()

# Read API Key
API_KEY = os.getenv("GEMINI_API_KEY")

print("API Key Loaded:", API_KEY is not None)
print("API Key:", API_KEY[:10] + "..." if API_KEY else "NOT FOUND")


# Create Gemini Client
client = genai.Client(api_key=API_KEY)

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