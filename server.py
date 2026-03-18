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

    contents = []

    for msg in req.messages:
        parts = []

        # Only add image if present (usually last user message)
        if msg.image:
            parts.append({
                "inline_data": {
                    "mime_type": msg.mime_type or "image/jpeg",
                    "data": msg.image
                }
            })

        if msg.content:
            parts.append({"text": msg.content})
        elif not msg.image:
            parts.append({"text": "..."})

        if parts:
            contents.append({
                "role": msg.role,
                "parts": parts
            })

    # Add system context at beginning
    system_ctx = [
        {
            "role": "user",
            "parts": [{"text": "انت مساعد ذكاء اصطناعي شخصي اسمك AI عبد الرحمن حمزه. تحدث دائما بالعربية. تستطيع تحليل الصور والاجابة على اي سؤال بشكل منطقي ومفيد."}]
        },
        {
            "role": "model",
            "parts": [{"text": "حسناً، أنا AI عبد الرحمن حمزه، جاهز لمساعدتك!"}]
        }
    ]

    data = {"contents": system_ctx + contents}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        return {"answer": answer}
    except Exception as e:
        return {"error": "حدث خطأ", "details": str(e)}