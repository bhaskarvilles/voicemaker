# Deploying VoiceMaker with Index-TTS2 to Render

This guide will help you deploy VoiceMaker with both Edge-TTS and Index-TTS2 to Render.

## Prerequisites

- GitHub account
- Render account (free tier works, but Standard plan recommended for Index-TTS2)
- Your VoiceMaker repository pushed to GitHub

## Quick Deployment Steps

### 1. Push Your Code to GitHub

```bash
cd c:\Users\bhask\Desktop\voicemaker

# Initialize git if not already done
git init
git add .
git commit -m "Add Index-TTS2 integration"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/voicemaker.git
git branch -M main
git push -u origin main
```

### 2. Create New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your `voicemaker` repository

### 3. Configure the Service

**Basic Settings**:
- **Name**: `voicemaker-app` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Runtime**: `Python 3`

**Build & Deploy**:
- **Build Command**: `bash build.sh`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

**Instance Type**:
- **Free Tier**: Works but Index-TTS2 will be slow (30-60s per generation)
- **Starter ($7/month)**: Recommended - much faster Index-TTS2 (10-20s per generation)
- **Standard ($25/month)**: Best performance (5-10s per generation)

### 4. Add Environment Variables

Click **"Advanced"** and add:

```
PYTHON_VERSION=3.11.0
```

### 5. Configure Disk Storage (Important!)

Index-TTS2 models need persistent storage:

1. Scroll to **"Disk"** section
2. Click **"Add Disk"**
3. Configure:
   - **Name**: `voicemaker-models`
   - **Mount Path**: `/opt/render/project/src/index-tts/checkpoints`
   - **Size**: `5 GB`

This ensures models persist between deployments.

### 6. Deploy!

1. Click **"Create Web Service"**
2. Render will start building your app
3. **First deployment takes 10-15 minutes** (downloading models)
4. Subsequent deployments are faster (~3-5 minutes)

### 7. Monitor Deployment

Watch the build logs:
- ✅ Installing Python dependencies
- ✅ Installing UV package manager
- ✅ Setting up Index-TTS2
- ✅ Downloading models (~2-3GB)
- ✅ Build completed

### 8. Access Your App

Once deployed, Render provides a URL like:
```
https://voicemaker-app.onrender.com
```

Visit it and you should see both engines available!

---

## Deployment Configuration Files

### `build.sh`
Automatically:
- Installs all dependencies
- Sets up Index-TTS2
- Downloads models from HuggingFace
- Falls back to ModelScope if needed

### `render.yaml` (Optional)
Infrastructure-as-code configuration. You can use this instead of manual setup:

1. Place `render.yaml` in your repository
2. On Render, click **"New +"** → **"Blueprint"**
3. Select your repository
4. Render will auto-configure everything!

---

## Performance Expectations

### Edge-TTS (All Plans)
- Synthesis: 1-2 seconds
- Always fast and reliable

### Index-TTS2 Performance by Plan

| Plan | CPU | RAM | Index-TTS2 Speed | Cost |
|------|-----|-----|------------------|------|
| Free | 0.5 CPU | 512MB | 30-60s | $0 |
| Starter | 1 CPU | 2GB | 10-20s | $7/mo |
| Standard | 2 CPU | 4GB | 5-10s | $25/mo |

**Recommendation**: Start with Free tier to test, upgrade to Starter for production.

---

## Troubleshooting

### Build Fails During Model Download

**Error**: `hf download` command fails

**Solution**: The build script automatically falls back to ModelScope. If both fail:
1. Check Render build logs
2. Ensure disk storage is configured
3. Try deploying again (network issues are temporary)

### Index-TTS2 Shows "Setup Required"

**Possible Causes**:
1. Models didn't download during build
2. Disk not mounted correctly
3. Build script failed

**Solution**:
1. Check build logs for errors
2. Verify disk is mounted at `/opt/render/project/src/index-tts/checkpoints`
3. Redeploy the service

### App is Slow/Timing Out

**For Index-TTS2**:
- Increase timeout in start command: `--timeout 180`
- Upgrade to Starter or Standard plan
- Use Edge-TTS for faster synthesis

**For Edge-TTS**:
- Should always be fast
- If slow, check Render status page

### Out of Memory Errors

**Solution**:
- Reduce workers: `--workers 1`
- Upgrade to plan with more RAM
- Index-TTS2 needs at least 2GB RAM

---

## Environment Variables (Optional)

Add these for fine-tuning:

```bash
# Python version
PYTHON_VERSION=3.11.0

# Gunicorn workers (adjust based on plan)
WEB_CONCURRENCY=2  # Free: 1, Starter: 2, Standard: 4

# Request timeout (seconds)
TIMEOUT=120  # Increase for Index-TTS2

# Flask environment
FLASK_ENV=production

# HuggingFace mirror (if in China)
HF_ENDPOINT=https://hf-mirror.com
```

---

## Updating Your Deployment

### Push Updates

```bash
git add .
git commit -m "Update description"
git push
```

Render auto-deploys on push (if auto-deploy enabled).

### Manual Deploy

1. Go to Render Dashboard
2. Select your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## Cost Optimization

### Free Tier Strategy
- Use Edge-TTS for most requests (fast, free)
- Use Index-TTS2 sparingly for special cases
- App spins down after 15 min inactivity (cold start ~30s)

### Paid Tier Benefits
- No spin-down
- Faster Index-TTS2
- More concurrent users
- Better reliability

---

## Monitoring

### Health Check
Your app has a health endpoint:
```
https://your-app.onrender.com/api/health
```

Returns:
```json
{
  "status": "healthy",
  "edge_tts_loaded": true,
  "index_tts_loaded": true
}
```

### Check Engine Status
```
https://your-app.onrender.com/api/engines
```

Shows which engines are available.

---

## Security Considerations

### CORS
Already configured in `app.py` for all origins. For production, restrict to your domain:

```python
CORS(app, origins=["https://yourdomain.com"])
```

### Rate Limiting
Consider adding rate limiting for production:

```bash
pip install flask-limiter
```

### API Keys
For production, add API key authentication to prevent abuse.

---

## Next Steps

1. ✅ Deploy to Render
2. ✅ Test both engines
3. ✅ Monitor performance
4. 📊 Add analytics (optional)
5. 🔒 Add authentication (optional)
6. 🌐 Add custom domain (optional)

---

## Support

- **Render Docs**: https://render.com/docs
- **VoiceMaker Issues**: Create issue in your GitHub repo
- **Index-TTS2 Support**: https://github.com/index-tts/index-tts

---

## Summary

Your VoiceMaker app is ready for deployment! The build script handles everything automatically:

✅ Edge-TTS works immediately  
✅ Index-TTS2 models download during build  
✅ Both engines available after deployment  
✅ Persistent storage for models  
✅ Auto-deploy on git push  

**Estimated first deployment time**: 10-15 minutes  
**Estimated subsequent deployments**: 3-5 minutes  

Happy deploying! 🚀
