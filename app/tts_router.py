from __future__ import annotations

import uuid
from pathlib import Path

import time
from app.cache import cache_key


import edge_tts
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
# from typing import Optional

router = APIRouter(tags=["tts"])

OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

DEFAULT_VOICE = "en-US-AriaNeural"  # English-only
# WAV/PCM (RIFF header) output format used by Microsoft TTS stacks :contentReference[oaicite:0]{index=0}
# WAV_OUTPUT_FORMAT = "riff-24khz-16bit-mono-pcm"
WAV_OUTPUT_FORMAT = "riff-16khz-16bit-mono-pcm"



class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    voice: str | None = None

    rate: str | None = None    # e.g. "+0%", "+15%", "-10%"
    pitch: str | None = None   # e.g. "+0Hz", "+30Hz", "-20Hz"
    volume: str | None = None  # e.g. "+0%", "+10%", "-5%"

# @router.post("/tts")
# async def tts(req: TTSRequest):
#     voice = req.voice or DEFAULT_VOICE
#     rate = req.rate or "+0%"
#     pitch = req.pitch or "+0Hz"
#     volume = req.volume or "+0%"

#     out_name = f"{uuid.uuid4().hex}.wav"
#     out_path = OUT_DIR / out_name

#     try:
#         communicate = edge_tts.Communicate(
#             req.text,
#             voice,
#             rate=rate,
#             pitch=pitch,
#             volume=volume,
#         )

#         await communicate.save(
#             str(out_path),
#             output_format=WAV_OUTPUT_FORMAT,
#         )

#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"TTS failed: {type(e).__name__}: {e}",
#         )

#     return FileResponse(
#         path=str(out_path),
#         media_type="audio/wav",
#         filename="speech.wav",
#     )


@router.post("/tts")
async def tts(req: TTSRequest):
    try:
        communicate = edge_tts.Communicate(
            req.text,
            DEFAULT_VOICE,
        )

        out_path = "debug.wav"
        await communicate.save(out_path)

        return FileResponse(
            path=out_path,
            media_type="audio/wav",
            filename="speech.wav",
        )

    except Exception as e:
        import traceback
        traceback.print_exc()   
        raise

from fastapi.responses import JSONResponse
from app.emotion import detect_emotion
from app.mapping import map_emotion, intensity_boost



class EmpathyRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
 

@router.post("/empathy")
async def empathy(req: EmpathyRequest):
    emo = detect_emotion(req.text)
    label = emo["label"]
    score = float(emo["score"])

    intensity = intensity_boost(req.text, score)
    cfg = map_emotion(label, intensity)

    # out_name = f"{uuid.uuid4().hex}.wav"
    # out_path = OUT_DIR / out_name
    # Cache filename from deterministic key
    key = cache_key(req.text, cfg, WAV_OUTPUT_FORMAT)
    out_name = f"{key[:24]}.wav"
    out_path = OUT_DIR / out_name


    if out_path.exists():
        return JSONResponse(
            {
                "emotion": {"label": label, "score": score, "intensity": intensity},
                "voice_params": cfg,
                "audio_url": f"/audio/{out_name}",
                "cached": True,
            }
        )


    tmp_name = f"{key[:24]}_{uuid.uuid4().hex}.tmp.wav"
    tmp_path = OUT_DIR / tmp_name

    try:
        communicate = edge_tts.Communicate(
            req.text,
            cfg["voice"],
            rate=cfg["rate"],
            pitch=cfg["pitch"],
            volume=cfg["volume"],
            # output_format=WAV_OUTPUT_FORMAT,
        )
        await communicate.save(str(tmp_path))


        if out_path.exists():
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass
        else:
            tmp_path.replace(out_path)

    except Exception as e:
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"TTS failed: {type(e).__name__}: {e}")

    return JSONResponse(
        {
            "emotion": {"label": label, "score": score, "intensity": intensity},
            "voice_params": cfg,
            "audio_url": f"/audio/{out_name}",
            "cached": False,
        }
    )



    # try:
    #     communicate = edge_tts.Communicate(
    #         req.text,
    #         cfg["voice"],
    #         rate=cfg["rate"],
    #         pitch=cfg["pitch"],
    #         volume=cfg["volume"],
    #     )

    #     # await communicate.save(
    #     #     str(out_path),
    #     #     output_format=WAV_OUTPUT_FORMAT,
    #     # )
    #     await communicate.save(str(out_path))


    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=f"TTS failed: {type(e).__name__}: {e}",
    #     )

    # return JSONResponse(
    #     {
    #         "emotion": {"label": label, "score": score, "intensity": intensity},
    #         "voice_params": cfg,
    #         "audio_url": f"/audio/{out_name}",
    #     }
    # )


@router.get("/audio/{file_name}")
def get_audio(file_name: str):
    path = OUT_DIR / file_name
    if not path.exists() or path.suffix.lower() != ".wav":
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(str(path), media_type="audio/wav", filename=file_name)


@router.post("/cleanup")
def cleanup(older_than_minutes: int = 60 * 24):

    cutoff = time.time() - (older_than_minutes * 60)
    deleted = 0
    kept = 0

    for p in OUT_DIR.glob("*.wav"):
        try:
            if p.stat().st_mtime < cutoff:
                p.unlink()
                deleted += 1
            else:
                kept += 1
        except Exception:
            kept += 1

    return {"deleted": deleted, "kept": kept, "older_than_minutes": older_than_minutes}
