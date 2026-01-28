#!/bin/bash
# Render Build Script for VoiceMaker with Index-TTS2
# This script runs during deployment to set up both Edge-TTS and Index-TTS2

set -e  # Exit on error

echo "======================================"
echo "VoiceMaker Deployment Build Script"
echo "======================================"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install UV package manager
echo "📦 Installing UV package manager..."
pip install uv

# Setup Index-TTS2
echo "🎭 Setting up Index-TTS2..."
cd index-tts

# Install Index-TTS2 dependencies
echo "📦 Installing Index-TTS2 dependencies..."
uv sync --extra webui --no-dev

# Download Index-TTS2 models
echo "⬇️  Downloading Index-TTS2 models (this may take 5-10 minutes)..."
uv tool install "huggingface-hub[cli,hf_xet]"

# Add uv tools to PATH
export PATH="$HOME/.local/bin:$PATH"

# Download models to checkpoints directory
echo "📥 Downloading IndexTTS-2 model files..."
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints || {
    echo "⚠️  HuggingFace download failed, trying ModelScope..."
    uv tool install "modelscope"
    modelscope download --model IndexTeam/IndexTTS-2 --local_dir checkpoints
}

cd ..

echo "✅ Build completed successfully!"
echo "======================================"
echo "Edge-TTS: Ready"
echo "Index-TTS2: Models downloaded"
echo "======================================"
