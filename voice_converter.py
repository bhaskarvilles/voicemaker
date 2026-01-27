"""
Voice Converter Module - Edge-TTS Version
Handles text-to-speech using Microsoft Edge TTS
"""

import os
import asyncio
import edge_tts
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceConverter:
    """
    Voice conversion engine using Microsoft Edge TTS
    """
    
    def __init__(self):
        """
        Initialize the voice converter with Edge TTS
        """
        logger.info("Initializing Voice Converter with Edge-TTS...")
        self.available_voices = []
        self._load_voices()
        logger.info(f"Voice Converter ready with {len(self.available_voices)} voices")
    
    def _load_voices(self):
        """Load available voices from Edge TTS"""
        try:
            # Get available voices synchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            voices = loop.run_until_complete(edge_tts.list_voices())
            loop.close()
            
            # Filter for high-quality neural voices
            self.available_voices = [
                {
                    'name': v['ShortName'],
                    'display_name': v['FriendlyName'],
                    'gender': v['Gender'],
                    'locale': v['Locale']
                }
                for v in voices
                if 'Neural' in v['ShortName']
            ]
            
            logger.info(f"Loaded {len(self.available_voices)} neural voices")
        except Exception as e:
            logger.error(f"Error loading voices: {e}")
            # Provide some default voices as fallback
            self.available_voices = [
                {'name': 'en-US-AriaNeural', 'display_name': 'Aria (US Female)', 'gender': 'Female', 'locale': 'en-US'},
                {'name': 'en-US-GuyNeural', 'display_name': 'Guy (US Male)', 'gender': 'Male', 'locale': 'en-US'},
                {'name': 'en-GB-SoniaNeural', 'display_name': 'Sonia (UK Female)', 'gender': 'Female', 'locale': 'en-GB'},
            ]
    
    def get_available_voices(self):
        """
        Get list of available voices
        
        Returns:
            List of voice dictionaries
        """
        return self.available_voices
    
    async def _generate_speech_async(self, text, voice_name, output_path):
        """
        Async method to generate speech
        """
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(output_path)
    
    def text_to_speech(self, text, voice_name, output_path):
        """
        Convert text to speech using specified voice
        
        Args:
            text: Text to convert to speech
            voice_name: Name of the voice to use (e.g., 'en-US-AriaNeural')
            output_path: Path to save the output audio
            
        Returns:
            Path to the generated audio file
        """
        try:
            logger.info(f"Converting text to speech with voice: {voice_name}")
            
            # Validate voice
            valid_voices = [v['name'] for v in self.available_voices]
            if voice_name not in valid_voices:
                logger.warning(f"Voice {voice_name} not found, using default")
                voice_name = 'en-US-AriaNeural'
            
            # Generate speech using asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._generate_speech_async(text, voice_name, output_path))
            loop.close()
            
            logger.info(f"Speech generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error in text-to-speech conversion: {e}")
            raise
    
    def validate_audio_file(self, audio_path):
        """
        Validate that the audio file exists and is readable
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            dict with validation results
        """
        try:
            if not os.path.exists(audio_path):
                return {'valid': False, 'error': 'File does not exist'}
            
            file_size = os.path.getsize(audio_path)
            
            return {
                'valid': True,
                'size': file_size,
                'path': audio_path
            }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }


if __name__ == "__main__":
    # Test the voice converter
    print("Testing Voice Converter with Edge-TTS...")
    try:
        vc = VoiceConverter()
        print(f"✓ Voice Converter initialized successfully")
        print(f"✓ Available voices: {len(vc.get_available_voices())}")
        
        # Show first 5 voices
        print("\nSample voices:")
        for voice in vc.get_available_voices()[:5]:
            print(f"  - {voice['display_name']} ({voice['name']})")
            
    except Exception as e:
        print(f"✗ Error: {e}")
