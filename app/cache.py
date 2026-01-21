import hashlib
import json


def cache_key(text: str, voice_params: dict, fmt: str) -> str:
    payload = {
        "text": text,
        "voice_params": voice_params,
        "format": fmt,
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
