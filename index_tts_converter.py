"""
Index-TTS2 Converter Module
Handles advanced voice cloning and emotional speech synthesis using Index-TTS2
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, List, Dict, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IndexTTSConverter:
    """
    Voice conversion engine using Index-TTS2
    Provides voice cloning and emotional speech synthesis
    """
    
    def __init__(self, model_dir: str = None, use_fp16: bool = False):
        """
        Initialize the Index-TTS2 converter
        
        Args:
            model_dir: Directory containing Index-TTS2 models
            use_fp16: Use half-precision for faster inference (CPU compatible)
        """
        logger.info("Initializing Index-TTS2 Converter...")
        
        self.model_dir = model_dir or self._get_default_model_dir()
        self.use_fp16 = use_fp16
        self.model = None
        self.is_available = False
        
        # Try to initialize Index-TTS2
        try:
            self._initialize_model()
            self.is_available = True
            logger.info("Index-TTS2 Converter ready")
        except Exception as e:
            logger.warning(f"Index-TTS2 not available: {e}")
            logger.info("Index-TTS2 features will be disabled. Please run setup.")
    
    def _get_default_model_dir(self) -> str:
        """Get default model directory"""
        base_dir = Path(__file__).parent
        return str(base_dir / "index-tts" / "checkpoints")
    
    def _initialize_model(self):
        """Initialize the Index-TTS2 model"""
        try:
            # Add index-tts to Python path
            index_tts_path = Path(__file__).parent / "index-tts"
            if index_tts_path.exists():
                sys.path.insert(0, str(index_tts_path))
            
            # Import Index-TTS2 modules
            from indextts.infer_v2 import IndexTTS2
            
            # Check if models exist
            config_path = Path(self.model_dir) / "config.yaml"
            if not config_path.exists():
                raise FileNotFoundError(
                    f"Index-TTS2 models not found at {self.model_dir}. "
                    "Please run the setup script to download models."
                )
            
            # Initialize model
            logger.info("Loading Index-TTS2 model (this may take a moment)...")
            self.model = IndexTTS2(
                cfg_path=str(config_path),
                model_dir=self.model_dir,
                use_fp16=self.use_fp16,
                use_cuda_kernel=False,  # CPU only
                use_deepspeed=False     # Not needed for CPU
            )
            
            logger.info("Index-TTS2 model loaded successfully")
            
        except ImportError as e:
            raise ImportError(
                f"Failed to import Index-TTS2 modules: {e}. "
                "Please ensure Index-TTS2 is properly installed."
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Index-TTS2: {e}")
    
    def clone_voice(
        self,
        text: str,
        reference_audio: str,
        output_path: str,
        language: str = "auto"
    ) -> str:
        """
        Clone a voice from reference audio
        
        Args:
            text: Text to synthesize
            reference_audio: Path to reference audio file (3-30 seconds)
            output_path: Path to save output audio
            language: Language code (auto-detected if "auto")
        
        Returns:
            Path to generated audio file
        """
        if not self.is_available:
            raise RuntimeError("Index-TTS2 is not available. Please run setup.")
        
        try:
            logger.info(f"Cloning voice with reference: {reference_audio}")
            
            # Validate reference audio
            if not os.path.exists(reference_audio):
                raise FileNotFoundError(f"Reference audio not found: {reference_audio}")
            
            # Generate speech
            self.model.infer(
                spk_audio_prompt=reference_audio,
                text=text,
                output_path=output_path,
                verbose=True
            )
            
            logger.info(f"Voice cloned successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error in voice cloning: {e}")
            raise
    
    def synthesize_with_emotion_audio(
        self,
        text: str,
        speaker_audio: str,
        emotion_audio: str,
        output_path: str,
        emotion_intensity: float = 1.0
    ) -> str:
        """
        Synthesize speech with emotional reference audio
        
        Args:
            text: Text to synthesize
            speaker_audio: Reference audio for speaker voice
            emotion_audio: Reference audio for emotional style
            output_path: Path to save output audio
            emotion_intensity: Emotion intensity (0.0-1.0)
        
        Returns:
            Path to generated audio file
        """
        if not self.is_available:
            raise RuntimeError("Index-TTS2 is not available. Please run setup.")
        
        try:
            logger.info(f"Synthesizing with emotion reference: {emotion_audio}")
            
            # Validate inputs
            if not os.path.exists(speaker_audio):
                raise FileNotFoundError(f"Speaker audio not found: {speaker_audio}")
            if not os.path.exists(emotion_audio):
                raise FileNotFoundError(f"Emotion audio not found: {emotion_audio}")
            
            # Clamp emotion intensity
            emotion_intensity = max(0.0, min(1.0, emotion_intensity))
            
            # Generate speech with emotion
            self.model.infer(
                spk_audio_prompt=speaker_audio,
                text=text,
                output_path=output_path,
                emo_audio_prompt=emotion_audio,
                emo_alpha=emotion_intensity,
                verbose=True
            )
            
            logger.info(f"Emotional speech generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error in emotional synthesis: {e}")
            raise
    
    def synthesize_with_emotion_vector(
        self,
        text: str,
        speaker_audio: str,
        emotion_vector: List[float],
        output_path: str,
        use_random: bool = False
    ) -> str:
        """
        Synthesize speech with emotion vector
        
        Args:
            text: Text to synthesize
            speaker_audio: Reference audio for speaker voice
            emotion_vector: 8-element list [happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]
            output_path: Path to save output audio
            use_random: Enable random sampling (reduces voice fidelity)
        
        Returns:
            Path to generated audio file
        """
        if not self.is_available:
            raise RuntimeError("Index-TTS2 is not available. Please run setup.")
        
        try:
            logger.info(f"Synthesizing with emotion vector: {emotion_vector}")
            
            # Validate inputs
            if not os.path.exists(speaker_audio):
                raise FileNotFoundError(f"Speaker audio not found: {speaker_audio}")
            
            if len(emotion_vector) != 8:
                raise ValueError("Emotion vector must have exactly 8 elements")
            
            # Normalize emotion vector
            emotion_vector = [max(0.0, min(1.0, e)) for e in emotion_vector]
            
            # Generate speech with emotion vector
            self.model.infer(
                spk_audio_prompt=speaker_audio,
                text=text,
                output_path=output_path,
                emo_vector=emotion_vector,
                use_random=use_random,
                verbose=True
            )
            
            logger.info(f"Emotional speech generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error in emotional synthesis: {e}")
            raise
    
    def validate_audio_file(self, audio_path: str) -> Dict:
        """
        Validate an audio file for use with Index-TTS2
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            dict with validation results
        """
        try:
            if not os.path.exists(audio_path):
                return {'valid': False, 'error': 'File does not exist'}
            
            file_size = os.path.getsize(audio_path)
            
            # Check file size (3-30 seconds recommended, ~50KB-5MB)
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
                'recommended': 10000 < file_size < 5000000  # 10KB - 5MB
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def get_emotion_labels(self) -> List[str]:
        """Get list of emotion labels in order"""
        return [
            "Happy",
            "Angry", 
            "Sad",
            "Afraid",
            "Disgusted",
            "Melancholic",
            "Surprised",
            "Calm"
        ]
    
    def is_model_available(self) -> bool:
        """Check if Index-TTS2 model is available"""
        return self.is_available


if __name__ == "__main__":
    # Test the Index-TTS2 converter
    print("Testing Index-TTS2 Converter...")
    try:
        converter = IndexTTSConverter()
        
        if converter.is_model_available():
            print("✓ Index-TTS2 Converter initialized successfully")
            print(f"✓ Model directory: {converter.model_dir}")
            print(f"✓ Emotion labels: {', '.join(converter.get_emotion_labels())}")
        else:
            print("✗ Index-TTS2 models not available")
            print("  Please run setup to download models")
            
    except Exception as e:
        print(f"✗ Error: {e}")
