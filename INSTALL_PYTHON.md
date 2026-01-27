# Installing Python 3.11 on Windows

## Current Situation
You currently have Python 3.13.2 installed, but Coqui TTS requires Python 3.8-3.11.

## Option 1: Download and Install Python 3.11 (Recommended)

### Step 1: Download Python 3.11
1. Go to: https://www.python.org/downloads/release/python-3119/
2. Scroll down to "Files" section
3. Download: **Windows installer (64-bit)** - `python-3.11.9-amd64.exe`

### Step 2: Install Python 3.11
1. Run the downloaded installer
2. ✅ **IMPORTANT**: Check "Add Python 3.11 to PATH"
3. Click "Install Now"
4. Wait for installation to complete

### Step 3: Verify Installation
Open a **new** PowerShell window and run:
```powershell
py -3.11 --version
```

You should see: `Python 3.11.9`

### Step 4: Create Virtual Environment
```powershell
cd c:\Users\bhask\Desktop\voicemaker
py -3.11 -m venv venv
```

### Step 5: Activate Virtual Environment
```powershell
.\venv\Scripts\activate
```

### Step 6: Install Dependencies
```powershell
pip install -r requirements.txt
```

This will take 5-10 minutes and download ~1-2GB of AI models.

### Step 7: Run the Application
```powershell
python app.py
```

Then open your browser to: http://localhost:5000

---

## Option 2: Use Windows Python Launcher (After Installing Python 3.11)

Once Python 3.11 is installed, you can use the `py` launcher:

```powershell
# Create venv with Python 3.11
py -3.11 -m venv venv

# Activate
.\venv\Scripts\activate

# Install
pip install -r requirements.txt

# Run
python app.py
```

---

## Option 3: Use Conda (Alternative)

If you have Anaconda or Miniconda installed:

```powershell
conda create -n voicemaker python=3.11
conda activate voicemaker
pip install -r requirements.txt
python app.py
```

---

## Troubleshooting

### "py -3.11 not found" after installation
- Close and reopen PowerShell
- Make sure you checked "Add to PATH" during installation
- Try running the installer again

### Multiple Python versions
- Use `py -3.11` to specifically target Python 3.11
- Use `py --list` to see all installed Python versions

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `py --list` | List all installed Python versions |
| `py -3.11 --version` | Check Python 3.11 version |
| `py -3.11 -m venv venv` | Create virtual environment |
| `.\venv\Scripts\activate` | Activate virtual environment |
| `deactivate` | Deactivate virtual environment |

---

## Next Steps

1. ✅ Download Python 3.11.9 from the link above
2. ✅ Install it (remember to check "Add to PATH")
3. ✅ Open a **new** PowerShell window
4. ✅ Run: `py -3.11 -m venv venv`
5. ✅ Continue with the setup

**Download Link**: https://www.python.org/downloads/release/python-3119/
