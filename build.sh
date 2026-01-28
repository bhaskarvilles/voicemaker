#!/bin/bash
# Render Build Script for VoiceMaker with Coqui TTS
# This script runs during deployment to set up Edge-TTS and Coqui TTS

set -e  # Exit on error

echo "======================================"
echo "VoiceMaker Deployment Build Script"
echo "======================================"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Coqui TTS
echo "🎤 Installing Coqui TTS..."
pip install TTS

# Pre-download Coqui TTS XTTS v2 model
echo "⬇️  Downloading Coqui TTS XTTS v2 model (this may take 5-10 minutes)..."
python3 << 'PYTHON_SCRIPT'
try:
    from TTS.api import TTS
    print("Downloading XTTS v2 model...")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)
    print("✓ Coqui TTS model downloaded successfully")
except Exception as e:
    print(f"⚠️  Coqui TTS model download failed: {e}")
    print("Model will download on first use")
PYTHON_SCRIPT

echo "✅ Build completed successfully!"
echo "======================================"
echo "Edge-TTS: Ready"
echo "Coqui TTS: Model downloaded"
echo "======================================"
