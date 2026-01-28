# Coqui TTS - Optional Installation

Due to Python version compatibility constraints, Coqui TTS is **optional** and not included in the main deployment.

## Why Optional?

Coqui TTS requires Python 3.9-3.11, and has complex dependencies that can cause deployment issues. To ensure reliable deployment of Edge-TTS and Index-TTS2, Coqui TTS is made optional.

## How to Install Coqui TTS (Optional)

### For Local Development

```powershell
# Install Coqui TTS
pip install TTS

# Test it
python coqui_tts_converter.py
```

### For Render Deployment

If you want to enable Coqui TTS on Render:

1. Add to `requirements.txt`:
   ```
   TTS>=0.21.0,<0.23.0
   ```

2. Ensure Python 3.11 in `render.yaml`:
   ```yaml
   PYTHON_VERSION: 3.11.0
   ```

3. Add to `build.sh` before the final echo:
   ```bash
   # Install Coqui TTS (optional)
   echo "🎤 Installing Coqui TTS..."
   pip install TTS || echo "⚠️  Coqui TTS installation failed (optional)"
   ```

4. Redeploy

## Current Status

**Deployed Engines**:
- ✅ **Edge-TTS**: Ready (300+ voices, fast)
- ✅ **Index-TTS2**: Ready (voice cloning, emotions)
- ⚠️ **Coqui TTS**: Optional (requires manual setup)

## Backend Support

The backend (`coqui_tts_converter.py` and `app.py`) is **already implemented** and ready. It will:
- Gracefully handle missing Coqui TTS
- Show as "unavailable" in `/api/engines`
- Work automatically once TTS package is installed

## Recommendation

**For Production**: Deploy with Edge-TTS and Index-TTS2 first. These provide excellent coverage:
- Edge-TTS: 100+ languages, 300+ voices
- Index-TTS2: Voice cloning, emotional control

**Add Coqui Later**: If you need the specific features (voice conversion, 1100+ languages), install it separately.

## Alternative: Local Coqui TTS

You can run Coqui TTS locally while using deployed Edge-TTS and Index-TTS2:

1. Install locally: `pip install TTS`
2. Run app locally for Coqui TTS features
3. Use deployed version for Edge-TTS and Index-TTS2

This gives you the best of both worlds!
