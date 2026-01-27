# VoiceMaker by Kerdos AI - AI Voice Conversion Application

**Developed by Kerdos Infrasoft Private Limited**

Transform audio and text into any voice using AI-powered voice cloning technology.

> **⚠️ IMPORTANT**: This application requires **Python 3.11 or lower**. Python 3.13 is not currently supported by Coqui TTS. See [PYTHON_VERSION.md](PYTHON_VERSION.md) for setup instructions.

## 🎯 Features

- **Voice Cloning**: Clone any voice from just 3-30 seconds of reference audio
- **Text-to-Speech**: Convert text to speech in the cloned voice
- **Audio-to-Audio**: Transform existing audio to match a reference voice
- **Modern UI**: Beautiful, responsive interface with glassmorphism design
- **Drag & Drop**: Easy file uploads with drag-and-drop support
- **Real-time Preview**: Listen to generated audio instantly

## 🚀 Quick Start

### Prerequisites

- **Python 3.8 - 3.11** (Python 3.13 is NOT supported - see [PYTHON_VERSION.md](PYTHON_VERSION.md))
- (Optional) CUDA-compatible GPU for faster processing

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd voicemaker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   > **Note**: First installation will download ~1-2GB of AI models. This is a one-time download.

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📖 How to Use

### Step 1: Upload Reference Voice
- Click or drag-and-drop an audio file (3-30 seconds recommended)
- This is the voice that will be cloned
- Supported formats: WAV, MP3, OGG, FLAC, M4A

### Step 2: Choose Conversion Mode

#### Text-to-Speech Mode
1. Switch to the "Text to Speech" tab
2. Enter the text you want to convert (up to 5000 characters)
3. Click "Convert to Speech"

#### Audio-to-Audio Mode
1. Switch to the "Audio to Audio" tab
2. Upload the audio file you want to convert
3. Click "Convert Audio"

### Step 3: Download Result
- Listen to the generated audio in the player
- Click "Download Audio" to save the result

## ⚙️ System Requirements

### Minimum Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8+
- **RAM**: 4GB
- **Storage**: 5GB free space

### Recommended for Best Performance
- **GPU**: CUDA-compatible NVIDIA GPU
- **RAM**: 8GB+
- **Storage**: 10GB free space

## 🔧 Performance Notes

- **With GPU**: 1-3 seconds per sentence
- **Without GPU (CPU only)**: 5-15 seconds per sentence
- **First run**: Slower due to model download and initialization

## 🎨 Technology Stack

- **Backend**: Python, Flask, Coqui TTS (XTTS v2)
- **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JavaScript
- **AI Model**: XTTS v2 (Multilingual voice cloning)

## 📝 Supported Audio Formats

**Input**: WAV, MP3, OGG, FLAC, M4A  
**Output**: WAV (high quality, uncompressed)

## ⚠️ Ethical Usage Guidelines

This tool can clone voices from short audio samples. Please ensure:

- ✅ You have permission to use any voice samples
- ✅ You comply with local laws regarding voice synthesis
- ✅ You use this technology responsibly and ethically
- ❌ Do not use for impersonation, fraud, or deception
- ❌ Do not create misleading or harmful content

## 🐛 Troubleshooting

### "Model loading failed"
- Ensure you have a stable internet connection for first-time model download
- Check that you have sufficient disk space (~5GB)

### "CUDA not available" warning
- This is normal if you don't have an NVIDIA GPU
- The application will use CPU (slower but functional)

### Slow processing
- First run is always slower (model initialization)
- Consider using a GPU for better performance
- Reduce text length or audio duration

### "Invalid audio file" error
- Ensure your audio file is in a supported format
- Try converting your audio to WAV format
- Check that the audio file is not corrupted

## 📄 API Endpoints

For developers who want to integrate programmatically:

### POST `/api/convert/text-to-speech`
Convert text to speech using a reference voice.

**Form Data**:
- `text`: Text to convert
- `reference_audio`: Reference audio file

**Response**: Audio file (WAV)

### POST `/api/convert/audio-to-audio`
Convert input audio to match reference voice.

**Form Data**:
- `input_audio`: Audio file to convert
- `reference_audio`: Reference audio file

**Response**: Audio file (WAV)

### GET `/api/health`
Check server health status.

**Response**: JSON with status information

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your needs.

## 📜 License

This project uses Coqui TTS which is licensed under the Mozilla Public License 2.0.

## 🙏 Acknowledgments

- **Coqui TTS**: For the amazing XTTS v2 model
- **Mozilla**: For supporting open-source TTS research

---

## 🏢 About Kerdos Infrasoft

**Kerdos Infrasoft Private Limited** is a cutting-edge technology company established in December 2023, based in Bengaluru, India. We specialize in:

- 🤖 **Artificial Intelligence & Machine Learning**
- ⛓️ **Blockchain Technology**
- 💬 **Natural Language Processing**
- 💻 **Advanced Software Development**

### Our Mission
Driving innovation and business growth across industries through cutting-edge AI, blockchain, and software solutions.

### Recognition
- ✅ Officially recognized under **Startup India Initiative** by the Government of India
- 🏆 CIN: U62099KA2023PTC182869

### Contact Us
- 🌐 **Website**: [kerdos.in](https://kerdos.in)
- 🎤 **Voice App**: [kerdos.sbs](https://kerdos.sbs)
- 📧 **Email**: info@kerdos.io
- 📍 **Location**: Bengaluru, Karnataka, India

### Our Technologies
We develop innovative solutions including:
- AI-powered applications and platforms
- Blockchain solutions for finance, healthcare, and supply chain
- Enterprise software and cloud solutions
- Data analytics and business intelligence tools

---

**Made with ❤️ by Kerdos Infrasoft using AI-powered voice technology**
