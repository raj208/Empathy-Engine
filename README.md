# The Empathy Engine

The **Empathy Engine** is a FastAPI service that takes text input, detects the **emotion** in the text, and generates **expressive speech** by modulating **voice parameters** (rate, pitch, volume) using **Edge-TTS**.  
It outputs a **playable `.wav`** file and provides a simple web UI for instant demo.


## Features Implemented

✅ **Text Input** via API + Web UI  
✅ **Emotion Detection** using a Hugging Face emotion classifier (7 emotion labels)  
✅ **Granular Emotions** (joy, anger, sadness, fear, surprise, disgust, neutral)  
✅ **Intensity Scaling** using model confidence + punctuation/caps/intensifiers  
✅ **Voice Parameter Modulation** (Rate + Pitch + Volume)  
✅ **Emotion → Voice Mapping** with clear rules per emotion  
✅ **WAV Output** (`riff-24khz-16bit-mono-pcm`)  
✅ **Caching** (same input + params returns same saved WAV)  
✅ **Cleanup Endpoint** to delete old generated WAV files


## Tech Stack

- **FastAPI** (API server)
- **Edge-TTS** (Text-to-Speech engine)
- **Hugging Face Transformers** (emotion classifier)
- **Torch (CPU)** (for running the transformer model locally)
- **Jinja2** (serving the demo UI)

## Project Structure

```
project/
├─ app/
│  ├─ main.py
│  ├─ emotion.py
│  ├─ mapping.py
│  ├─ cache.py
│  ├─ tts_router.py
│  └─ ui_router.py
│
├─ templates/
│  └─ index.html
│
├─ outputs/        # Generated WAV files are saved here
│
└─ README.md
```

## Setup Instructions (Windows)

### 1) Create and activate a virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

---



### 3) Install dependencies
```powershell
pip install -r requirements.txt
```

---


### 5) Run the application
```powershell
uvicorn app.main:app
```

The app will start at:
```
http://127.0.0.1:8000
```

---

## Notes
- Generated audio files are saved in the `outputs/` directory

