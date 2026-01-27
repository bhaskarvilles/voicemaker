# VoiceMaker - Installation Issues & Solutions

## ⚠️ Coqui TTS Installation Failed

Unfortunately, Coqui TTS cannot be installed on your system due to build errors on Windows with Python 3.11. This is a known issue with the package.

## ✅ Alternative Solution: Edge-TTS

I'm implementing an alternative solution using **Microsoft Edge TTS** which:
- ✅ Works perfectly on Windows
- ✅ No complex dependencies or build requirements
- ✅ Supports multiple high-quality voices
- ✅ Completely free and open-source
- ⚠️ Does NOT support custom voice cloning from audio samples

### What Changed

**Original Plan (Coqui TTS)**:
- Upload reference audio → Clone voice → Convert text/audio

**New Plan (Edge-TTS)**:
- Select from pre-built voices → Convert text to speech
- High-quality neural voices from Microsoft
- Multiple languages and voice styles

## 📦 What's Installed

✅ PyTorch 2.10.0 (CPU version)  
✅ Flask 3.1.2 (Web server)  
✅ Flask-CORS (API support)  
✅ Audio libraries (pydub, soundfile, librosa)  
🔄 Edge-TTS (installing...)  

## 🎯 Next Steps

1. Finish installing edge-tts
2. Update `voice_converter.py` to use edge-tts instead of Coqui TTS
3. Update the UI to show voice selection instead of reference upload
4. Test the application

## 🔮 Future Options

If you really need custom voice cloning, you have these options:

1. **Use a cloud service**:
   - ElevenLabs API (paid, excellent quality)
   - Resemble.ai (paid, good for production)
   
2. **Try on Linux/Mac**:
   - Coqui TTS works better on Linux
   - Use WSL2 (Windows Subsystem for Linux)

3. **Use Docker**:
   - Run Coqui TTS in a Docker container
   - Pre-built images available

Would you like me to:
- A) Continue with Edge-TTS (simpler, works now)
- B) Set up a cloud-based solution (requires API key)
- C) Try Docker/WSL2 approach (more complex setup)
