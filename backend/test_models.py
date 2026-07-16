from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for model in client.models.list():
    print(model.name)

print("\nModels supporting generateContent:\n")

for model in client.models.list():
    methods = getattr(model, "supported_actions", [])
    if methods:
        print(model.name, methods)