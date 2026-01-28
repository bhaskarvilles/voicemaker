# Index-TTS2 Setup Guide

This guide will help you set up Index-TTS2 for advanced voice cloning and emotional speech synthesis in VoiceMaker.

## Prerequisites

- Python 3.8-3.11 (already installed for VoiceMaker)
- UV package manager (automatically installed)
- 3-5GB free disk space for models
- Internet connection for model download

## Quick Setup

### Step 1: Download Index-TTS2 Models

The Index-TTS2 repository is already cloned in the `index-tts` directory. Now you need to download the models:

```powershell
# Navigate to the index-tts directory
cd index-tts

# Install dependencies
uv sync --extra webui

# Download models from HuggingFace
uv tool install "huggingface-hub[cli,hf_xet]"
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints
```

**Alternative**: Download from ModelScope (faster in some regions):

```powershell
uv tool install "modelscope"
modelscope download --model IndexTeam/IndexTTS-2 --local_dir checkpoints
```

### Step 2: Verify Installation

Test that Index-TTS2 is working:

```powershell
# From the voicemaker directory
cd ..
python index_tts_converter.py
```

You should see:
```
✓ Index-TTS2 Converter initialized successfully
✓ Model directory: c:\Users\...\voicemaker\index-tts\checkpoints
✓ Emotion labels: Happy, Angry, Sad, Afraid, Disgusted, Melancholic, Surprised, Calm
```

### Step 3: Start VoiceMaker

```powershell
python app.py
```

Open your browser to `http://localhost:5000` and you should see both engines available!

## Features

### Voice Cloning
- Upload 3-30 seconds of reference audio
- System will clone the voice characteristics
- Works with any language

### Emotional Control

**Three Modes**:

1. **No Emotion**: Simple voice cloning without emotional modification
2. **Audio Reference**: Upload an emotional reference audio to guide the emotion
3. **Manual Control**: Adjust 8 emotion sliders:
   - 😊 Happy
   - 😠 Angry
   - 😢 Sad
   - 😨 Afraid
   - 🤢 Disgusted
   - 😔 Melancholic
   - 😲 Surprised
   - 😌 Calm

## Troubleshooting

### Models Not Found

If you see "Index-TTS2 models not available":

1. Check that `index-tts/checkpoints/config.yaml` exists
2. Verify models were downloaded completely
3. Re-run the download command

### Slow Performance

Index-TTS2 runs on CPU (no GPU required) but is slower than Edge-TTS:
- First generation: 10-30 seconds
- Subsequent generations: 5-15 seconds
- This is normal for CPU-only operation

### Import Errors

If you see Python import errors:

```powershell
cd index-tts
uv sync --extra webui
```

This reinstalls all dependencies.

## Performance Tips

1. **Keep reference audio short**: 5-10 seconds is optimal
2. **Use clear audio**: Less background noise = better results
3. **Shorter text**: Break long text into smaller chunks
4. **Emotion intensity**: Start with 60-80% for more natural results

## Supported Audio Formats

- **Input**: WAV, MP3, OGG, FLAC, M4A
- **Output**: WAV (high quality, uncompressed)

## API Usage

### Voice Cloning Endpoint

```bash
curl -X POST http://localhost:5000/api/index-tts/clone-voice \
  -F "text=Hello, this is a test" \
  -F "reference_audio=@voice.wav"
```

### Emotional Synthesis (Manual)

```bash
curl -X POST http://localhost:5000/api/index-tts/synthesize-emotion \
  -F "text=I am so happy!" \
  -F "speaker_audio=@voice.wav" \
  -F "emotion_mode=manual" \
  -F "emotion_vector=[0.8,0,0,0,0,0,0,0]"
```

### Emotional Synthesis (Audio Reference)

```bash
curl -X POST http://localhost:5000/api/index-tts/synthesize-emotion \
  -F "text=This is amazing!" \
  -F "speaker_audio=@voice.wav" \
  -F "emotion_mode=audio" \
  -F "emotion_audio=@happy.wav" \
  -F "emotion_intensity=0.8"
```

## Comparison: Edge-TTS vs Index-TTS2

| Feature | Edge-TTS | Index-TTS2 |
|---------|----------|------------|
| Setup | No setup required | Model download required |
| Voices | 300+ pre-built | Clone any voice |
| Speed | Very fast (1-2s) | Slower (5-30s) |
| Quality | High | Very High |
| Emotions | Limited | Full control |
| Languages | 100+ | Any language |
| GPU Required | No | No (but recommended) |

## Advanced Configuration

### Enable FP16 (Faster Inference)

Edit `index_tts_converter.py` line 40:

```python
index_tts_converter = IndexTTSConverter(use_fp16=True)  # Enable FP16
```

This uses half-precision for faster inference with minimal quality loss.

### Custom Model Directory

Set a custom model directory in `index_tts_converter.py`:

```python
converter = IndexTTSConverter(model_dir="path/to/your/models")
```

## Getting Help

- **Index-TTS2 GitHub**: https://github.com/index-tts/index-tts
- **Discord**: https://discord.gg/uT32E7KDmy
- **Email**: indexspeech@bilibili.com

## Credits

Index-TTS2 is developed by the IndexTeam at Bilibili. This integration is part of VoiceMaker by Kerdos AI.
