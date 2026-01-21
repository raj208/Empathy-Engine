from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.tts_router import router as tts_router
from app.emotion import load_emotion_model, detect_emotion
from app.ui_router import router as ui_router


app = FastAPI(title="Empathy Engine", version="0.1")

app.include_router(tts_router)
app.include_router(ui_router)




class TextIn(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


@app.on_event("startup")
def _startup():
    load_emotion_model()


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/analyze")
def analyze(payload: TextIn):
    return detect_emotion(payload.text)
