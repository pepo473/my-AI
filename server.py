import os
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional

API_KEY = "AIzaSyA3hhlgH0f6qJtDQ9wCZjpTlde74MU7cGw"

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str
    image: Optional[str] = None
    mime_type: Optional[str] = "image/jpeg"

class ChatRequest(BaseModel):
    messages: List[Message]

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/ask")
async def ask_ai(req: ChatRequest):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}

    system = {
        "role": "user",
        "parts": [{"text": "انت مساعد ذكاء اصطناعي شخصي اسمك 'AI عبد الرحمن حمزه'. تحدث دائما بالعربية. تستطيع تحليل الصور والاجابة على اي سؤال."}]
    }
    system_reply = {
        "role": "model",
        "parts": [{"text": "حسناً، أنا AI عبد الرحمن حمزه، جاهز لمساعدتك!"}]
    }

    contents = [system, system_reply]

    for msg in req.messages:
        parts = []
        if msg.image:
            parts.append({
                "inline_data": {
                    "mime_type": msg.mime_type,
                    "data": msg.image
                }
            })
        parts.append({"text": msg.content or "حلل هذه الصورة"})
        contents.append({"role": msg.role, "parts": parts})

    data = {"contents": contents}
    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    try:
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        return {"answer": answer}
    except KeyError:
        return {"error": "حدث خطأ", "details": result}