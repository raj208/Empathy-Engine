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