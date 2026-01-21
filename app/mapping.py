import re


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def intensity_boost(text: str, base: float) -> float:

    t = text.strip()

    ex = t.count("!")
    qm = t.count("?")


    caps_words = re.findall(r"\b[A-Z]{3,}\b", t)
    caps = len(caps_words)

    elongated = len(re.findall(r"([a-zA-Z])\1{2,}", t))


    intensifiers = re.findall(r"\b(very|really|extremely|super|so|totally|absolutely)\b", t.lower())
    ints = len(intensifiers)



    boost = 0.0
    boost += min(0.25, 0.05 * ex)       
    boost += min(0.12, 0.04 * qm)        
    boost += min(0.18, 0.06 * caps)      
    boost += min(0.12, 0.04 * elongated) 
    boost += min(0.12, 0.03 * ints)      

    return _clamp(base + boost)


def _fmt_pct(x: float) -> str:

    s = int(round(x))
    return f"{s:+d}%"


def _fmt_hz(x: float) -> str:
    s = int(round(x))
    return f"{s:+d}Hz"


def map_emotion(label: str, intensity: float) -> dict:

    i = _clamp(intensity)

    def lerp(a: float, b: float) -> float:
        return a + (b - a) * i

  
    voice_by_emotion = {
        "joy": "en-US-AriaNeural",
        "neutral": "en-US-AriaNeural",
        "sadness": "en-US-GuyNeural",
        "anger": "en-US-GuyNeural",
        "fear": "en-US-JennyNeural",
        "surprise": "en-US-JennyNeural",
        "disgust": "en-US-GuyNeural",
    }


    if label == "joy":
        rate = lerp(10, 28)
        pitch = lerp(12, 48)
        vol = lerp(4, 14)
    elif label == "sadness":
        rate = -lerp(8, 22)
        pitch = -lerp(10, 40)
        vol = -lerp(2, 10)
    elif label == "anger":
        rate = lerp(8, 25)
        pitch = lerp(-5, 10)     
        vol = lerp(10, 22)
    elif label == "fear":
        rate = lerp(6, 18)
        pitch = lerp(18, 55)
        vol = lerp(-4, 4)
    elif label == "surprise":
        rate = lerp(12, 30)
        pitch = lerp(20, 60)
        vol = lerp(4, 12)
    elif label == "disgust":
        rate = -lerp(4, 16)
        pitch = -lerp(8, 28)
        vol = lerp(0, 10)
    else:  
        rate = 0
        pitch = 0
        vol = 0

    return {
        "voice": voice_by_emotion.get(label, "en-US-AriaNeural"),
        "rate": _fmt_pct(rate),
        "pitch": _fmt_hz(pitch),
        "volume": _fmt_pct(vol),
    }

