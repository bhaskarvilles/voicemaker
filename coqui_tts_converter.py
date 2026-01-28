"""
Coqui TTS Converter Module
Handles multilingual TTS, voice cloning, and voice conversion using Coqui TTS
"""

import os
import logging
from pathlib import Path
from typing import Optional, List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CoquiTTSConverter:
    """
    Voice conversion engine using Coqui TTS
    Provides multilingual TTS, voice cloning, and voice conversion
    """
    
    def __init__(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"):
        """
        Initialize the Coqui TTS converter
        
        Args:
            model_name: Coqui TTS model to use (default: XTTS v2 for voice cloning)
        """
        logger.info("Initializing Coqui TTS Converter...")
        
        self.model_name = model_name
        self.tts = None
        self.is_available = False
        self.device = "cpu"  # Will auto-detect GPU if available
        
        # Try to initialize Coqui TTS
        try:
            self._initialize_model()
            self.is_available = True
            logger.info(f"Coqui TTS Converter ready with model: {model_name}")
        except Exception as e:
            logger.warning(f"Coqui TTS not available: {e}")
            logger.info("Coqui TTS features will be disabled.")
    
    def _initialize_model(self):
        """Initialize the Coqui TTS model"""
        try:
            import torch
            from TTS.api import TTS
            
            # Detect device
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Using device: {self.device}")
            
            # Initialize TTS model
            logger.info(f"Loading Coqui TTS model: {self.model_name}")
            logger.info("This may take a moment on first run (downloading model)...")
            
            self.tts = TTS(self.model_name, progress_bar=False).to(self.device)
            
            logger.info("Coqui TTS model loaded successfully")
            
        except ImportError as e:
            raise ImportError(
                f"Failed to import Coqui TTS: {e}. "
                "Please install with: pip install TTS"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Coqui TTS: {e}")
    
    def synthesize(
        self,
        text: str,
        output_path: str,
        language: str = "en"
    ) -> str:
        """
        Basic text-to-speech synthesis
        
        Args:
            text: Text to synthesize
            output_path: Path to save output audio
            language: Language code (e.g., 'en', 'es', 'fr')
        
        Returns:
            Path to generated audio file
        """
        if not self.is_available:
            raise RuntimeError("Coqui TTS is not available.")
        
        try:
            logger.info(f"Synthesizing text in language: {language}")
            
            # For single-speaker models
            if "multilingual" not in self.model_name:
                self.tts.tts_to_file(text=text, file_path=output_path)
            else:
                # For multilingual models, language is required
                self.tts.tts_to_file(text=text, language=language, file_path=output_path)
            
            logger.info(f"Speech synthesized: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error in synthesis: {e}")
            raise
    
    def clone_voice(
        self,
        text: str,
        speaker_wav: str,
        output_path: str,
        language: str = "en"
    ) -> str:
        """
        Clone a voice from reference audio
        
        Args:
            text: Text to synthesize
            speaker_wav: Path to reference audio file (3-30 seconds)
            output_path: Path to save output audio
            language: Language code
        
        Returns:
            Path to generated audio file
        """
        if not self.is_available:
            raise RuntimeError("Coqui TTS is not available.")
        
        try:
            logger.info(f"Cloning voice from: {speaker_wav}")
            
            # Validate reference audio
            if not os.path.exists(speaker_wav):
                raise FileNotFoundError(f"Reference audio not found: {speaker_wav}")
            
            # Generate speech with voice cloning
            self.tts.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language=language,
                file_path=output_path
            )
            
            logger.info(f"Voice cloned successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error in voice cloning: {e}")
            raise
    
    def convert_voice(
        self,
        source_wav: str,
        target_wav: str,
        output_path: str
    ) -> str:
        """
        Convert voice from source to target speaker
        
        Args:
            source_wav: Path to source audio file
            target_wav: Path to target voice audio file
            output_path: Path to save output audio
        
        Returns:
            Path to generated audio file
        """
        if not self.is_available:
            raise RuntimeError("Coqui TTS is not available.")
        
        try:
            logger.info(f"Converting voice from {source_wav} to {target_wav}")
            
            # Validate inputs
            if not os.path.exists(source_wav):
                raise FileNotFoundError(f"Source audio not found: {source_wav}")
            if not os.path.exists(target_wav):
                raise FileNotFoundError(f"Target audio not found: {target_wav}")
            
            # Check if current model supports voice conversion
            if "voice_conversion" not in self.model_name:
                # Use TTS with voice conversion as fallback
                logger.info("Using TTS with voice conversion")
                self.tts.tts_with_vc_to_file(
                    text="",  # Empty for voice conversion
                    speaker_wav=target_wav,
                    file_path=output_path
                )
            else:
                # Use dedicated voice conversion model
                self.tts.voice_conversion_to_file(
                    source_wav=source_wav,
                    target_wav=target_wav,
                    file_path=output_path
                )
            
            logger.info(f"Voice converted successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error in voice conversion: {e}")
            raise
    
    @staticmethod
    def list_available_models() -> List[Dict]:
        """
        List available Coqui TTS models
        
        Returns:
            List of model information dictionaries
        """
        try:
            from TTS.api import TTS
            
            # Get all available models
            all_models = TTS().list_models()
            
            # Curate popular models
            popular_models = [
                {
                    "id": "tts_models/multilingual/multi-dataset/xtts_v2",
                    "name": "XTTS v2",
                    "description": "Multilingual voice cloning (recommended)",
                    "features": ["voice_cloning", "multilingual"],
                    "languages": ["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn", "ja", "hu", "ko"]
                },
                {
                    "id": "tts_models/multilingual/multi-dataset/your_tts",
                    "name": "YourTTS",
                    "description": "Voice cloning in English, French, Portuguese",
                    "features": ["voice_cloning", "multilingual"],
                    "languages": ["en", "fr-fr", "pt-br"]
                },
                {
                    "id": "tts_models/en/ljspeech/vits",
                    "name": "VITS (English)",
                    "description": "High-quality English TTS",
                    "features": ["high_quality"],
                    "languages": ["en"]
                },
                {
                    "id": "voice_conversion_models/multilingual/vctk/freevc24",
                    "name": "FreeVC",
                    "description": "Voice conversion model",
                    "features": ["voice_conversion"],
                    "languages": ["multilingual"]
                }
            ]
            
            return popular_models
            
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    @staticmethod
    def get_supported_languages() -> List[Dict]:
        """
        Get list of supported languages
        
        Returns:
            List of language dictionaries with code and name
        """
        # Popular languages supported by XTTS v2
        languages = [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"},
            {"code": "it", "name": "Italian"},
            {"code": "pt", "name": "Portuguese"},
            {"code": "pl", "name": "Polish"},
            {"code": "tr", "name": "Turkish"},
            {"code": "ru", "name": "Russian"},
            {"code": "nl", "name": "Dutch"},
            {"code": "cs", "name": "Czech"},
            {"code": "ar", "name": "Arabic"},
            {"code": "zh-cn", "name": "Chinese (Simplified)"},
            {"code": "ja", "name": "Japanese"},
            {"code": "hu", "name": "Hungarian"},
            {"code": "ko", "name": "Korean"},
            {"code": "hi", "name": "Hindi"}
        ]
        
        return languages
    
    def switch_model(self, model_name: str):
        """
        Switch to a different Coqui TTS model
        
        Args:
            model_name: Name of the model to switch to
        """
        try:
            logger.info(f"Switching to model: {model_name}")
            self.model_name = model_name
            self._initialize_model()
            logger.info("Model switched successfully")
        except Exception as e:
            logger.error(f"Error switching model: {e}")
            raise
    
    def is_model_available(self) -> bool:
        """Check if Coqui TTS model is available"""
        return self.is_available
    
    def validate_audio_file(self, audio_path: str) -> Dict:
        """
        Validate an audio file for use with Coqui TTS
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            dict with validation results
        """
        try:
            if not os.path.exists(audio_path):
                return {'valid': False, 'error': 'File does not exist'}
            
            file_size = os.path.getsize(audio_path)
            
            # Check file size (3-30 seconds recommended)
            if file_size < 10000:  # Less than 10KB
                return {
                    'valid': False,
                    'error': 'Audio file too small (minimum 3 seconds recommended)'
                }
            
            if file_size > 50 * 1024 * 1024:  # More than 50MB
                return {
                    'valid': False,
                    'error': 'Audio file too large (maximum 50MB)'
                }
            
            return {
                'valid': True,
                'size': file_size,
                'path': audio_path,
                'recommended': 10000 < file_size < 5000000
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }


if __name__ == "__main__":
    # Test the Coqui TTS converter
    print("Testing Coqui TTS Converter...")
    try:
        converter = CoquiTTSConverter()
        
        if converter.is_model_available():
            print("✓ Coqui TTS Converter initialized successfully")
            print(f"✓ Model: {converter.model_name}")
            print(f"✓ Device: {converter.device}")
            
            # List available models
            models = CoquiTTSConverter.list_available_models()
            print(f"✓ Available models: {len(models)}")
            for model in models:
                print(f"  - {model['name']}: {model['description']}")
            
            # List supported languages
            languages = CoquiTTSConverter.get_supported_languages()
            print(f"✓ Supported languages: {len(languages)}")
            print(f"  Languages: {', '.join([lang['name'] for lang in languages[:10]])}...")
        else:
            print("✗ Coqui TTS not available")
            print("  Please install with: pip install TTS")
            
    except Exception as e:
        print(f"✗ Error: {e}")
