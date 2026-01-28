"""
Voice Conversion Web Application
Developed by Kerdos Infrasoft Private Limited
Flask server providing API endpoints for voice cloning and conversion
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from voice_converter import VoiceConverter
from index_tts_converter import IndexTTSConverter
from coqui_tts_converter import CoquiTTSConverter
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

# Initialize voice converters (lazy loading)
voice_converter = None
index_tts_converter = None
coqui_tts_converter = None


def get_voice_converter():
    """Lazy load the Edge-TTS voice converter"""
    global voice_converter
    if voice_converter is None:
        logger.info("Loading Edge-TTS voice converter...")
        voice_converter = VoiceConverter()
        logger.info("Edge-TTS voice converter ready")
    return voice_converter


def get_index_tts_converter():
    """Lazy load the Index-TTS2 converter"""
    global index_tts_converter
    if index_tts_converter is None:
        logger.info("Loading Index-TTS2 converter...")
        index_tts_converter = IndexTTSConverter(use_fp16=False)  # CPU mode
        logger.info("Index-TTS2 converter ready")
    return index_tts_converter


def get_coqui_tts_converter():
    """Lazy load the Coqui TTS converter"""
    global coqui_tts_converter
    if coqui_tts_converter is None:
        logger.info("Loading Coqui TTS converter...")
        coqui_tts_converter = CoquiTTSConverter()  # Auto-detects GPU
        logger.info("Coqui TTS converter ready")
    return coqui_tts_converter


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
        'edge_tts_loaded': voice_converter is not None,
        'index_tts_loaded': index_tts_converter is not None,
        'coqui_tts_loaded': coqui_tts_converter is not None
    })


@app.route('/api/engines', methods=['GET'])
def get_engines():
    """
    Get list of available TTS engines
    """
    try:
        # Check Index-TTS2 availability
        index_available = False
        try:
            converter = get_index_tts_converter()
            index_available = converter.is_model_available()
        except:
            pass
        
        # Check Coqui TTS availability
        coqui_available = False
        try:
            converter = get_coqui_tts_converter()
            coqui_available = converter.is_model_available()
        except:
            pass
        
        engines = [
            {
                'id': 'edge-tts',
                'name': 'Edge-TTS',
                'description': '300+ pre-built neural voices',
                'features': ['Multiple languages', 'Fast synthesis', 'No setup required'],
                'available': True
            },
            {
                'id': 'index-tts2',
                'name': 'Index-TTS2',
                'description': 'Advanced voice cloning and emotional synthesis',
                'features': ['Voice cloning', 'Emotional control', 'High quality'],
                'available': index_available
            },
            {
                'id': 'coqui-tts',
                'name': 'Coqui TTS',
                'description': 'Multilingual voice cloning (1100+ languages)',
                'features': ['Voice cloning', 'Voice conversion', 'Multilingual'],
                'available': coqui_available
            }
        ]
        
        return jsonify({
            'engines': engines,
            'total': len(engines)
        })
        
    except Exception as e:
        logger.error(f"Error getting engines: {e}")
        return jsonify({'error': str(e)}), 500


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


@app.route('/api/index-tts/clone-voice', methods=['POST'])
def index_tts_clone_voice():
    """
    Clone a voice using Index-TTS2
    
    Expected form data:
    - text: Text to synthesize
    - reference_audio: Reference audio file for voice cloning
    """
    try:
        # Validate inputs
        if 'text' not in request.form:
            return jsonify({'error': 'No text provided'}), 400
        
        if 'reference_audio' not in request.files:
            return jsonify({'error': 'No reference audio provided'}), 400
        
        text = request.form['text']
        reference_file = request.files['reference_audio']
        
        # Validate text
        if not text or len(text.strip()) == 0:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text too long (max 5000 characters)'}), 400
        
        # Save reference audio
        if reference_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(reference_file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        ref_filename = secure_filename(reference_file.filename)
        ref_path = os.path.join(app.config['UPLOAD_FOLDER'], f'ref_{ref_filename}')
        reference_file.save(ref_path)
        
        # Generate output path
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_index_tts.wav')
        
        # Clone voice
        logger.info(f"Cloning voice with Index-TTS2: {text[:50]}...")
        converter = get_index_tts_converter()
        
        if not converter.is_model_available():
            return jsonify({
                'error': 'Index-TTS2 models not available. Please run setup.'
            }), 503
        
        converter.clone_voice(text, ref_path, output_path)
        
        # Clean up reference file
        os.remove(ref_path)
        
        # Send the generated audio file
        return send_file(
            output_path,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='cloned_voice.wav'
        )
        
    except Exception as e:
        logger.error(f"Error in voice cloning: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/index-tts/synthesize-emotion', methods=['POST'])
def index_tts_synthesize_emotion():
    """
    Synthesize speech with emotional control using Index-TTS2
    
    Expected form data:
    - text: Text to synthesize
    - speaker_audio: Reference audio for speaker voice
    - emotion_mode: 'none', 'audio', or 'vector'
    - emotion_audio: (optional) Reference audio for emotion
    - emotion_vector: (optional) JSON array of 8 emotion values
    - emotion_intensity: (optional) Emotion intensity 0.0-1.0
    """
    try:
        # Validate inputs
        if 'text' not in request.form:
            return jsonify({'error': 'No text provided'}), 400
        
        if 'speaker_audio' not in request.files:
            return jsonify({'error': 'No speaker audio provided'}), 400
        
        text = request.form['text']
        speaker_file = request.files['speaker_audio']
        emotion_mode = request.form.get('emotion_mode', 'none')
        
        # Validate text
        if not text or len(text.strip()) == 0:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        # Save speaker audio
        if speaker_file.filename == '':
            return jsonify({'error': 'No speaker file selected'}), 400
        
        if not allowed_file(speaker_file.filename):
            return jsonify({'error': 'Invalid speaker file type'}), 400
        
        spk_filename = secure_filename(speaker_file.filename)
        spk_path = os.path.join(app.config['UPLOAD_FOLDER'], f'spk_{spk_filename}')
        speaker_file.save(spk_path)
        
        # Generate output path
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_emotion.wav')
        
        converter = get_index_tts_converter()
        
        if not converter.is_model_available():
            return jsonify({
                'error': 'Index-TTS2 models not available. Please run setup.'
            }), 503
        
        # Handle different emotion modes
        if emotion_mode == 'audio' and 'emotion_audio' in request.files:
            # Emotion from audio reference
            emotion_file = request.files['emotion_audio']
            emo_filename = secure_filename(emotion_file.filename)
            emo_path = os.path.join(app.config['UPLOAD_FOLDER'], f'emo_{emo_filename}')
            emotion_file.save(emo_path)
            
            emotion_intensity = float(request.form.get('emotion_intensity', 1.0))
            
            logger.info(f"Synthesizing with emotion audio: {text[:50]}...")
            converter.synthesize_with_emotion_audio(
                text, spk_path, emo_path, output_path, emotion_intensity
            )
            
            os.remove(emo_path)
            
        elif emotion_mode == 'vector' and 'emotion_vector' in request.form:
            # Emotion from vector
            import json
            emotion_vector = json.loads(request.form['emotion_vector'])
            
            logger.info(f"Synthesizing with emotion vector: {text[:50]}...")
            converter.synthesize_with_emotion_vector(
                text, spk_path, emotion_vector, output_path
            )
            
        else:
            # No emotion - simple voice cloning
            logger.info(f"Synthesizing without emotion: {text[:50]}...")
            converter.clone_voice(text, spk_path, output_path)
        
        # Clean up speaker file
        os.remove(spk_path)
        
        # Send the generated audio file
        return send_file(
            output_path,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='emotional_speech.wav'
        )
        
    except Exception as e:
        logger.error(f"Error in emotional synthesis: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/index-tts/emotions', methods=['GET'])
def get_emotions():
    """
    Get list of available emotions for Index-TTS2
    """
    try:
        converter = get_index_tts_converter()
        emotions = converter.get_emotion_labels()
        
        return jsonify({
            'emotions': emotions,
            'total': len(emotions)
        })
        
    except Exception as e:
        logger.error(f"Error getting emotions: {e}")
        return jsonify({'error': str(e)}), 500


# ===== Coqui TTS Endpoints =====

@app.route('/api/coqui/models', methods=['GET'])
def get_coqui_models():
    """
    Get list of available Coqui TTS models
    """
    try:
        models = CoquiTTSConverter.list_available_models()
        
        return jsonify({
            'models': models,
            'total': len(models)
        })
        
    except Exception as e:
        logger.error(f"Error getting Coqui models: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/coqui/languages', methods=['GET'])
def get_coqui_languages():
    """
    Get list of supported languages for Coqui TTS
    """
    try:
        languages = CoquiTTSConverter.get_supported_languages()
        
        return jsonify({
            'languages': languages,
            'total': len(languages)
        })
        
    except Exception as e:
        logger.error(f"Error getting languages: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/coqui/synthesize', methods=['POST'])
def coqui_synthesize():
    """
    Basic text-to-speech synthesis with Coqui TTS
    """
    try:
        # Get parameters
        text = request.form.get('text')
        language = request.form.get('language', 'en')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Get converter
        converter = get_coqui_tts_converter()
        
        if not converter.is_model_available():
            return jsonify({'error': 'Coqui TTS model not available'}), 503
        
        # Generate output path
        output_path = os.path.join(UPLOAD_FOLDER, f'coqui_output_{os.urandom(8).hex()}.wav')
        
        # Synthesize
        logger.info(f"Synthesizing with Coqui TTS: {text[:50]}...")
        converter.synthesize(text, output_path, language)
        
        # Return audio file
        return send_file(
            output_path,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='coqui_speech.wav'
        )
        
    except Exception as e:
        logger.error(f"Error in Coqui synthesis: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/coqui/clone-voice', methods=['POST'])
def coqui_clone_voice():
    """
    Voice cloning with Coqui TTS
    """
    try:
        # Get parameters
        text = request.form.get('text')
        language = request.form.get('language', 'en')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Get speaker audio file
        if 'speaker_audio' not in request.files:
            return jsonify({'error': 'Speaker audio file is required'}), 400
        
        speaker_file = request.files['speaker_audio']
        if speaker_file.filename == '':
            return jsonify({'error': 'No speaker audio file selected'}), 400
        
        if not allowed_file(speaker_file.filename):
            return jsonify({'error': 'Invalid audio file format'}), 400
        
        # Save speaker audio
        speaker_filename = secure_filename(f'speaker_{os.urandom(8).hex()}.wav')
        speaker_path = os.path.join(UPLOAD_FOLDER, speaker_filename)
        speaker_file.save(speaker_path)
        
        # Get converter
        converter = get_coqui_tts_converter()
        
        if not converter.is_model_available():
            return jsonify({'error': 'Coqui TTS model not available'}), 503
        
        # Generate output path
        output_path = os.path.join(UPLOAD_FOLDER, f'coqui_cloned_{os.urandom(8).hex()}.wav')
        
        # Clone voice
        logger.info(f"Cloning voice with Coqui TTS in language: {language}")
        converter.clone_voice(text, speaker_path, output_path, language)
        
        # Cleanup
        if os.path.exists(speaker_path):
            os.remove(speaker_path)
        
        # Return audio file
        return send_file(
            output_path,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='coqui_cloned_voice.wav'
        )
        
    except Exception as e:
        logger.error(f"Error in Coqui voice cloning: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/coqui/convert-voice', methods=['POST'])
def coqui_convert_voice():
    """
    Voice conversion with Coqui TTS
    """
    try:
        # Get source audio file
        if 'source_audio' not in request.files:
            return jsonify({'error': 'Source audio file is required'}), 400
        
        source_file = request.files['source_audio']
        if source_file.filename == '':
            return jsonify({'error': 'No source audio file selected'}), 400
        
        # Get target audio file
        if 'target_audio' not in request.files:
            return jsonify({'error': 'Target audio file is required'}), 400
        
        target_file = request.files['target_audio']
        if target_file.filename == '':
            return jsonify({'error': 'No target audio file selected'}), 400
        
        if not allowed_file(source_file.filename) or not allowed_file(target_file.filename):
            return jsonify({'error': 'Invalid audio file format'}), 400
        
        # Save audio files
        source_filename = secure_filename(f'source_{os.urandom(8).hex()}.wav')
        source_path = os.path.join(UPLOAD_FOLDER, source_filename)
        source_file.save(source_path)
        
        target_filename = secure_filename(f'target_{os.urandom(8).hex()}.wav')
        target_path = os.path.join(UPLOAD_FOLDER, target_filename)
        target_file.save(target_path)
        
        # Get converter
        converter = get_coqui_tts_converter()
        
        if not converter.is_model_available():
            return jsonify({'error': 'Coqui TTS model not available'}), 503
        
        # Generate output path
        output_path = os.path.join(UPLOAD_FOLDER, f'coqui_converted_{os.urandom(8).hex()}.wav')
        
        # Convert voice
        logger.info("Converting voice with Coqui TTS")
        converter.convert_voice(source_path, target_path, output_path)
        
        # Cleanup
        if os.path.exists(source_path):
            os.remove(source_path)
        if os.path.exists(target_path):
            os.remove(target_path)
        
        # Return audio file
        return send_file(
            output_path,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='coqui_converted_voice.wav'
        )
        
    except Exception as e:
        logger.error(f"Error in Coqui voice conversion: {e}")
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
