# Python Version Compatibility Notice

## ⚠️ Important: Python Version Requirement

The Coqui TTS library currently **does not support Python 3.13**. 

### Recommended Solution

**Option 1: Use Python 3.11 (Recommended)**

1. Install Python 3.11 from [python.org](https://www.python.org/downloads/)
2. Create a virtual environment:
   ```bash
   python3.11 -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**Option 2: Use Conda (Alternative)**

```bash
conda create -n voicemaker python=3.11
conda activate voicemaker
pip install -r requirements.txt
```

### Supported Python Versions

- ✅ Python 3.8
- ✅ Python 3.9
- ✅ Python 3.10
- ✅ Python 3.11
- ❌ Python 3.12 (limited support)
- ❌ Python 3.13 (not supported)

### Why This Happens

Coqui TTS depends on specific versions of PyTorch and other deep learning libraries that have not yet been compiled for Python 3.13. This is common with AI/ML libraries that require native extensions.

### Quick Test

After setting up Python 3.11, test the installation:

```bash
python -c "from TTS.api import TTS; print('✓ TTS installed successfully')"
```

If you see the success message, you're ready to run the application!
