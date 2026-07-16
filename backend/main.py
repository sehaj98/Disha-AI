from fastapi import FastAPI
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

# Request model
class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Welcome to Disha AI Backend!"}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.message,
        )

        return {
            "response": response.text
        }

    except Exception as e:
        print("Gemini Error:", e)
        return {
            "error": str(e)
        }