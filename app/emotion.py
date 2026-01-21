from transformers import pipeline

MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

_emoter = None


def load_emotion_model():
    global _emoter
    if _emoter is None:
        _emoter = pipeline(
            task="text-classification",
            model=MODEL_NAME,
            top_k=None,   
        )
    return _emoter


def detect_emotion(text: str) -> dict:
    emoter = load_emotion_model()
    out = emoter(text)[0] 
    out = sorted(out, key=lambda x: x["score"], reverse=True)
    top = out[0]
    label = top["label"]
    score = float(top["score"])

    intensity = score

    return {"label": label, "score": score, "intensity": intensity}
