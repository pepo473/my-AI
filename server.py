import os
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

API_KEY = "AIzaSyA3hhlgH0f6qJtDQ9wCZjpTlde74MU7cGw"

app = FastAPI()

class Question(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/ask")
async def ask_ai(question: Question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    system_prompt = "انت مساعد ذكاء اصطناعي شخصي اسمك AI عبد الرحمن حمزه. تحدث دائما بالعربية وكن مفيدا."
    data = {"contents": [{"parts": [{"text": system_prompt + "\n\n" + question.text}]}]}
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    try:
        return {"answer": result["candidates"][0]["content"]["parts"][0]["text"]}
    except KeyError:
        return {"error": "حدث خطأ", "details": result}