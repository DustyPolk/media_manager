#!/usr/bin/env python3
"""
Demo script showing how to use Media File Manager programmatically.
This script demonstrates the core functionality without requiring command line arguments.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from media.audio_processor import AudioProcessor
from media.format_detector import FormatDetector
from core.metadata_handler import MetadataHandler

def demo_audio_processing():
    """Demonstrate the audio processing capabilities."""
    print("🎵 Media File Manager - Audio Processing Demo")
    print("=" * 50)
    
    # Configuration
    config = {
        'supported_formats': {
            'audio': ['.mp3', '.flac', '.ogg', '.wav', '.aac', '.m4a'],
            'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']
        }
    }
    
    # Initialize components
    print("🔧 Initializing components...")
    format_detector = FormatDetector(config)
    audio_processor = AudioProcessor(config)
    metadata_handler = MetadataHandler(config)
    
    print("✅ All components initialized successfully!")
    
    # Example usage patterns
    print("\n📚 Example Usage Patterns:")
    print("-" * 30)
    
    print("\n1️⃣  Format Detection:")
    print("   format = format_detector.detect_format(file_path)")
    
    print("\n2️⃣  Metadata Extraction:")
    print("   metadata = audio_processor.extract_metadata(file_path)")
    
    print("\n3️⃣  Audio Properties:")
    print("   properties = audio_processor.get_audio_properties(file_path)")
    
    print("\n4️⃣  Metadata Update:")
    print("   success = audio_processor.update_metadata(file_path, new_metadata)")
    
    print("\n5️⃣  Using Metadata Handler (recommended):")
    print("   metadata = metadata_handler.extract_metadata(file_path)")
    
    # Show supported formats
    print("\n🎯 Supported Audio Formats:")
    for fmt in config['supported_formats']['audio']:
        print(f"   • {fmt}")
    
    print("\n🎯 Supported Video Formats:")
    for fmt in config['supported_formats']['video']:
        print(f"   • {fmt}")
    
    print("\n" + "=" * 50)
    print("💡 To test with a real MP3 file, run:")
    print("   python test_audio_file.py <path_to_your_mp3>")
    print("\n🎉 Demo complete!")

if __name__ == "__main__":
    demo_audio_processing()
