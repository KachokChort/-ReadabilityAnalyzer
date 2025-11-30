from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from functions import english, russian
import uvicorn

app = FastAPI(title="Readability API", version="1.0")

class TextRequest(BaseModel):
    text: str
    language: str


@app.get("/")
def index():
    return {"message": "Readability Calculator API", "status": "running"}


@app.post("/text/")
async def analyze_text(request: TextRequest):
    text = request.text.strip()
    language = request.language.lower()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if language == "english":
        result = english(text)
    elif language == "russian":
        result = russian(text)
    else:
        raise HTTPException(status_code=400, detail="Invalid language. Use 'english' or 'russian'")

    if result is None:
        raise HTTPException(status_code=400, detail="Could not analyze text")


    if result >= 90:
        level = "Very Easy"
    elif result >= 80:
        level = "Easy"
    elif result >= 70:
        level = "Fairly Easy"
    elif result >= 60:
        level = "Standard"
    elif result >= 50:
        level = "Fairly Difficult"
    elif result >= 30:
        level = "Difficult"
    else:
        level = "Very Confusing"

    return {
        "score": result,
        "level": level,
        "language": language
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
