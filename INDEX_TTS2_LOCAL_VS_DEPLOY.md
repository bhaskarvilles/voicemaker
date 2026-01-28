# ⚠️ Index-TTS2 Local vs Deployment

## What You're Seeing Locally

If you see **"Index-TTS2 requires setup"** or **"Deploy to Enable"** when running locally, this is **completely normal** and **expected**!

## Why This Happens

Index-TTS2 models are **2-3GB** in size. Instead of downloading them locally, they will be automatically downloaded during deployment to Render.

## How It Works

### Locally (Development)
- ✅ Edge-TTS works immediately
- ⚠️ Index-TTS2 shows "Deploy to Enable"
- This is intentional - no local setup needed!

### On Render (Production)
- ✅ Edge-TTS works immediately  
- ✅ Index-TTS2 models download automatically during build
- ✅ Both engines available after ~10-15 minute build

## The Build Process

When you deploy to Render, `build.sh` automatically:

1. Installs Python dependencies
2. Installs UV package manager
3. Downloads Index-TTS2 models (~2-3GB)
4. Saves models to persistent disk
5. Starts the application

**No manual intervention required!**

## What You Need to Do

### For Local Development
- Just use Edge-TTS (it works great!)
- Or deploy to Render to test Index-TTS2

### For Deployment
1. Push code to GitHub
2. Connect to Render
3. **Important**: Add disk storage (5GB) for models
4. Deploy and wait ~15 minutes
5. Both engines will be ready!

## Testing Locally (Optional)

If you really want to test Index-TTS2 locally:

```powershell
cd index-tts
uv sync --extra webui
uv tool install "huggingface-hub[cli,hf_xet]"
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints
```

This downloads ~2-3GB to your local machine.

## Summary

**The message you're seeing is correct!** 

- Local: Use Edge-TTS for development
- Deployed: Both engines work automatically

No action needed - just deploy when ready! 🚀

---

See [RENDER_DEPLOY_INDEX_TTS.md](RENDER_DEPLOY_INDEX_TTS.md) for full deployment guide.
