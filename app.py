"""
Voice Conversion Web Application
Developed by Kerdos Infrasoft Private Limited
Flask server providing API endpoints for voice cloning and conversion
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from voice_converter import VoiceConverter
import os
import tempfile
import logging
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize voice converter (lazy loading)
voice_converter = None


def get_voice_converter():
    """Lazy load the voice converter to avoid loading model on import"""
    global voice_converter
    if voice_converter is None:
        logger.info("Loading voice converter model...")
        voice_converter = VoiceConverter()
        logger.info("Voice converter ready")
    return voice_converter


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS


@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('static', 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': voice_converter is not None
    })


@app.route('/api/voices', methods=['GET'])
def get_voices():
    """
    Get list of available voices
    """
    try:
        vc = get_voice_converter()
        voices = vc.get_available_voices()
        
        # Group by locale for better organization
        grouped = {}
        for voice in voices:
            locale = voice['locale']
            if locale not in grouped:
                grouped[locale] = []
            grouped[locale].append(voice)
        
        return jsonify({
            'voices': voices,
            'grouped': grouped,
            'total': len(voices)
        })
        
    except Exception as e:
        logger.error(f"Error getting voices: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/convert/text-to-speech', methods=['POST'])
def text_to_speech():
    """
    Convert text to speech using selected voice
    
    Expected form data:
    - text: Text to convert
    - voice: Voice name to use (e.g., 'en-US-AriaNeural')
    """
    try:
        # Validate inputs
        if 'text' not in request.form:
            return jsonify({'error': 'No text provided'}), 400
        
        if 'voice' not in request.form:
            return jsonify({'error': 'No voice selected'}), 400
        
        text = request.form['text']
        voice_name = request.form['voice']
        
        # Validate text
        if not text or len(text.strip()) == 0:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text too long (max 5000 characters)'}), 400
        
        # Generate output path
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_tts.mp3')
        
        # Convert text to speech
        logger.info(f"Converting text to speech with voice {voice_name}: {text[:50]}...")
        vc = get_voice_converter()
        vc.text_to_speech(text, voice_name, output_path)
        
        # Send the generated audio file
        return send_file(
            output_path,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='converted_speech.mp3'
        )
        
    except Exception as e:
        logger.error(f"Error in text-to-speech conversion: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate-audio', methods=['POST'])
def validate_audio():
    """
    Validate an audio file
    
    Expected form data:
    - audio: Audio file to validate
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(audio_file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save temporarily
        filename = secure_filename(audio_file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_{filename}')
        audio_file.save(temp_path)
        
        # Validate
        vc = get_voice_converter()
        validation = vc.validate_audio_file(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify(validation)
        
    except Exception as e:
        logger.error(f"Error validating audio: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("VoiceMaker by Kerdos AI - Voice Conversion Application")
    print("=" * 60)
    print("Developed by: Kerdos Infrasoft Private Limited")
    print("Website: https://kerdos.in")
    print("Email: info@kerdos.in")
    print("-" * 60)
    print("\nStarting server...")
    print("Access the application at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
