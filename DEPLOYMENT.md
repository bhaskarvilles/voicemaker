# 🚀 VoiceMaker Deployment Guide

Complete guide to deploy your VoiceMaker application and share it with the public.

## 📋 Table of Contents

1. [Quick Comparison](#quick-comparison)
2. [Option 1: Render (Recommended - Free)](#option-1-render-recommended)
3. [Option 2: Railway](#option-2-railway)
4. [Option 3: Heroku](#option-3-heroku)
5. [Option 4: PythonAnywhere](#option-4-pythonanywhere)
6. [Option 5: Vercel + Serverless](#option-5-vercel)
7. [Option 6: Self-Hosting (VPS)](#option-6-self-hosting)
8. [Pre-Deployment Checklist](#pre-deployment-checklist)

---

## 🎯 Quick Comparison

| Platform | Free Tier | Ease | Best For | Limitations |
|----------|-----------|------|----------|-------------|
| **Render** | ✅ Yes | ⭐⭐⭐⭐⭐ | Beginners | Sleeps after 15min inactivity |
| **Railway** | ✅ $5 credit | ⭐⭐⭐⭐ | Developers | Credit runs out |
| **Heroku** | ❌ Paid only | ⭐⭐⭐⭐ | Production | No free tier |
| **PythonAnywhere** | ✅ Limited | ⭐⭐⭐ | Python apps | Limited resources |
| **Vercel** | ✅ Yes | ⭐⭐⭐ | Frontend | Backend limitations |
| **VPS** | ❌ Paid | ⭐⭐ | Full control | Requires setup |

---

## 🌟 Option 1: Render (Recommended)

**Best for**: Beginners, free hosting, automatic deployments

### Why Render?
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy GitHub integration
- ✅ Auto-deploys on git push
- ⚠️ Sleeps after 15 minutes of inactivity (wakes up in ~30 seconds)

### Step-by-Step Deployment

#### 1. Prepare Your App

Create `render.yaml` in your project root:

```yaml
services:
  - type: web
    name: voicemaker
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

#### 2. Update `requirements.txt`

Add Gunicorn for production:

```txt
Flask==3.1.2
flask-cors==6.0.2
edge-tts==7.2.7
gunicorn==21.2.0
```

#### 3. Create Production Config

Update `app.py` to use production settings:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

#### 4. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/voicemaker.git
git push -u origin main
```

#### 5. Deploy on Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: voicemaker
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click "Create Web Service"

**Your app will be live at**: `https://voicemaker.onrender.com`

---

## 🚂 Option 2: Railway

**Best for**: Quick deployments with $5 free credit

### Deployment Steps

#### 1. Add `Procfile`

```
web: gunicorn app:app
```

#### 2. Add `runtime.txt`

```
python-3.11.0
```

#### 3. Deploy

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys

**Your app will be live at**: `https://voicemaker-production.up.railway.app`

---

## 🔷 Option 3: Heroku

**Best for**: Production apps (paid only now)

### Deployment Steps

#### 1. Install Heroku CLI

```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### 2. Create Heroku App

```bash
heroku login
heroku create voicemaker-app
```

#### 3. Add Files

Create `Procfile`:
```
web: gunicorn app:app
```

Create `runtime.txt`:
```
python-3.11.0
```

#### 4. Deploy

```bash
git push heroku main
heroku open
```

**Cost**: ~$7/month for basic dyno

---

## 🐍 Option 4: PythonAnywhere

**Best for**: Python-specific hosting

### Deployment Steps

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files via "Files" tab
3. Create a virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 voicemaker
   pip install -r requirements.txt
   ```
4. Configure web app in "Web" tab
5. Set WSGI configuration to point to your `app.py`

**Free tier**: Limited CPU, good for testing

---

## ⚡ Option 5: Vercel

**Best for**: Frontend + serverless backend

### Deployment Steps

#### 1. Create `vercel.json`

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

#### 2. Deploy

```bash
npm i -g vercel
vercel
```

**Limitations**: Serverless functions have 10-second timeout

---

## 🖥️ Option 6: Self-Hosting (VPS)

**Best for**: Full control, custom domain

### Recommended Providers

- **DigitalOcean**: $6/month droplet
- **Linode**: $5/month
- **AWS Lightsail**: $3.50/month
- **Vultr**: $2.50/month

### Deployment Steps

#### 1. Set Up Server

```bash
# SSH into your server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Python 3.11
apt install python3.11 python3.11-venv nginx -y
```

#### 2. Upload Your App

```bash
# On your local machine
scp -r voicemaker root@your-server-ip:/var/www/
```

#### 3. Set Up Environment

```bash
cd /var/www/voicemaker
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 4. Create Systemd Service

Create `/etc/systemd/system/voicemaker.service`:

```ini
[Unit]
Description=VoiceMaker Flask App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/voicemaker
Environment="PATH=/var/www/voicemaker/venv/bin"
ExecStart=/var/www/voicemaker/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/voicemaker`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /var/www/voicemaker/static;
    }
}
```

#### 6. Start Services

```bash
systemctl enable voicemaker
systemctl start voicemaker
systemctl enable nginx
systemctl restart nginx
```

#### 7. Add HTTPS (Optional but Recommended)

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

---

## ✅ Pre-Deployment Checklist

Before deploying, make sure you have:

### 1. **Update `app.py` for Production**

```python
import os

# At the bottom of app.py
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
```

### 2. **Create `.gitignore`**

```
venv/
__pycache__/
*.pyc
.env
uploads/
*.wav
*.mp3
.DS_Store
```

### 3. **Add Security Headers**

Update `app.py`:

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

### 4. **Set Environment Variables**

Create `.env` file (don't commit this):

```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=10485760
```

### 5. **Test Locally in Production Mode**

```bash
export FLASK_ENV=production
gunicorn app:app
```

---

## 🎯 Recommended Deployment Path

For most users, I recommend this progression:

1. **Start with Render** (free, easy)
   - Perfect for testing and sharing with friends
   - No credit card required
   - Automatic HTTPS

2. **Upgrade to Railway** (if you need always-on)
   - $5 free credit
   - No sleep mode
   - Better performance

3. **Move to VPS** (for serious projects)
   - Full control
   - Custom domain
   - Better pricing at scale

---

## 📊 Cost Comparison

| Users/Month | Render | Railway | VPS |
|-------------|--------|---------|-----|
| 0-100 | Free | Free ($5 credit) | $5/month |
| 100-1000 | Free* | $5-10/month | $10/month |
| 1000+ | $7/month | $20/month | $20/month |

*With sleep mode

---

## 🔒 Security Considerations

1. **Never commit sensitive data**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Rate limiting** (for production)
   ```bash
   pip install flask-limiter
   ```

3. **CORS configuration**
   - Update allowed origins in production

4. **HTTPS only**
   - All platforms provide free SSL
   - Enforce HTTPS redirects

---

## 📝 Custom Domain Setup

Once deployed, you can add a custom domain:

### For Render/Railway/Heroku:
1. Buy domain from Namecheap/GoDaddy
2. Add CNAME record: `www` → `your-app.onrender.com`
3. Add A record: `@` → Platform's IP
4. Configure custom domain in platform settings

### For VPS:
1. Point A record to your server IP
2. Update Nginx configuration
3. Run Certbot for SSL

---

## 🎉 Post-Deployment

After deployment:

1. **Test all features**
   - Voice selection
   - Text-to-speech conversion
   - Audio download

2. **Monitor performance**
   - Check response times
   - Monitor error logs

3. **Share your app!**
   - Social media
   - Product Hunt
   - Reddit (r/SideProject)

---

## 🆘 Troubleshooting

### App won't start
- Check logs: `heroku logs --tail` or platform equivalent
- Verify Python version in `runtime.txt`
- Ensure all dependencies in `requirements.txt`

### Slow performance
- Enable caching
- Use CDN for static files
- Upgrade to paid tier

### Out of memory
- Reduce worker count
- Optimize voice model loading
- Upgrade server resources

---

## 📚 Additional Resources

- [Flask Deployment Docs](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)
- [Nginx Best Practices](https://www.nginx.com/blog/nginx-best-practices/)

---

## 🎊 Ready to Deploy?

**My recommendation**: Start with **Render** today!

1. Push your code to GitHub
2. Connect to Render
3. Deploy in 5 minutes
4. Share your app URL!

Good luck! 🚀
