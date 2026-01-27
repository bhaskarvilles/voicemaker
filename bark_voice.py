"""
Voice Cloning Module - Bark Integration
Provides expressive text-to-speech with different speaker voices
Note: Bark uses pre-defined speaker prompts, not true voice cloning from audio
"""

import os
import numpy as np
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BarkVoiceGenerator:
    """
    Voice generation using Bark TTS
    Supports multiple speaker voices and expressive speech
    """
    
    def __init__(self):
        """
        Initialize Bark voice generator
        """
        logger.info("Initializing Bark Voice Generator...")
        self.sample_rate = SAMPLE_RATE
        self.is_loaded = False
        logger.info("Bark Voice Generator ready (models will load on first use)")
    
    def _ensure_models_loaded(self):
        """Load Bark models if not already loaded"""
        if not self.is_loaded:
            logger.info("Loading Bark models (this may take a minute on first run)...")
            preload_models()
            self.is_loaded = True
            logger.info("Bark models loaded successfully")
    
    def get_available_speakers(self):
        """
        Get list of available Bark speaker presets
        
        Returns:
            List of speaker preset names
        """
        # Bark has pre-defined speaker prompts
        # Format: v2/{language}_{speaker}_{number}
        speakers = []
        
        # English speakers
        for i in range(10):
            speakers.append({
                'id': f'v2/en_speaker_{i}',
                'name': f'English Speaker {i}',
                'language': 'en',
                'description': 'English voice with natural intonation'
            })
        
        # Add some specific character voices
        speakers.extend([
            {'id': 'v2/en_speaker_0', 'name': 'Narrator (Male)', 'language': 'en', 'description': 'Deep, authoritative voice'},
            {'id': 'v2/en_speaker_1', 'name': 'Narrator (Female)', 'language': 'en', 'description': 'Clear, professional voice'},
            {'id': 'v2/en_speaker_6', 'name': 'Cheerful (Male)', 'language': 'en', 'description': 'Upbeat, energetic voice'},
            {'id': 'v2/en_speaker_9', 'name': 'Calm (Female)', 'language': 'en', 'description': 'Soothing, gentle voice'},
        ])
        
        return speakers
    
    def text_to_speech(self, text, speaker_id, output_path):
        """
        Convert text to speech using Bark
        
        Args:
            text: Text to convert (supports [laughter], [sighs], etc.)
            speaker_id: Speaker preset ID (e.g., 'v2/en_speaker_0')
            output_path: Path to save the output audio
            
        Returns:
            Path to the generated audio file
        """
        try:
            logger.info(f"Generating speech with Bark speaker: {speaker_id}")
            
            # Ensure models are loaded
            self._ensure_models_loaded()
            
            # Generate audio with speaker prompt
            audio_array = generate_audio(text, history_prompt=speaker_id)
            
            # Convert to 16-bit PCM
            audio_array = (audio_array * 32767).astype(np.int16)
            
            # Save as WAV file
            write_wav(output_path, self.sample_rate, audio_array)
            
            logger.info(f"Speech generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error in Bark text-to-speech: {e}")
            raise
    
    def text_to_speech_expressive(self, text, emotion, output_path):
        """
        Generate expressive speech with emotions
        
        Args:
            text: Text to convert
            emotion: Emotion to express (happy, sad, excited, calm, etc.)
            output_path: Path to save the output audio
            
        Returns:
            Path to the generated audio file
        """
        try:
            # Add emotion markers to text
            emotion_markers = {
                'happy': '[laughs] ',
                'excited': '♪ ',
                'sad': '[sighs] ',
                'calm': '',
                'surprised': '!',
            }
            
            marker = emotion_markers.get(emotion.lower(), '')
            enhanced_text = f"{marker}{text}"
            
            # Use default speaker
            return self.text_to_speech(enhanced_text, 'v2/en_speaker_1', output_path)
            
        except Exception as e:
            logger.error(f"Error in expressive speech generation: {e}")
            raise


if __name__ == "__main__":
    # Test the Bark voice generator
    print("Testing Bark Voice Generator...")
    try:
        generator = BarkVoiceGenerator()
        print(f"✓ Bark Voice Generator initialized")
        
        speakers = generator.get_available_speakers()
        print(f"✓ Available speakers: {len(speakers)}")
        
        print("\nSample speakers:")
        for speaker in speakers[:5]:
            print(f"  - {speaker['name']} ({speaker['id']})")
            
        # Test generation (commented out to avoid long model download during testing)
        # print("\nGenerating test audio...")
        # generator.text_to_speech("Hello, this is a test.", "v2/en_speaker_0", "test_bark.wav")
        # print("✓ Test audio generated")
            
    except Exception as e:
        print(f"✗ Error: {e}")
