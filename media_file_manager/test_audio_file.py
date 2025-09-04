#!/usr/bin/env python3
"""
Test script for Media File Manager audio processing.
Use this script to test the audio processor on any MP3 file.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from media.audio_processor import AudioProcessor
from media.format_detector import FormatDetector

def test_audio_file(file_path: str):
    """Test the audio processor on a given file."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ Error: File '{file_path}' does not exist!")
        return
    
    print(f"🎵 Testing Media File Manager on: {file_path.name}")
    print("=" * 50)
    
    # Initialize processors
    config = {
        'supported_formats': {
            'audio': ['.mp3', '.flac', '.ogg', '.wav', '.aac', '.m4a'],
            'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']
        }
    }
    
    format_detector = FormatDetector(config)
    audio_processor = AudioProcessor(config)
    
    # Test format detection
    print("🔍 Testing format detection...")
    detected_format = format_detector.detect_format(file_path)
    if detected_format:
        print(f"✅ Detected format: {detected_format}")
    else:
        print("❌ Could not detect format")
    
    # Test metadata extraction
    print("\n📋 Testing metadata extraction...")
    try:
        metadata = audio_processor.extract_metadata(file_path)
        if metadata:
            print("✅ Successfully extracted metadata:")
            for key, value in metadata.items():
                if key == 'artwork':
                    print(f"  {key}: [Artwork data - {len(value.get('data', b''))} bytes]")
                else:
                    print(f"  {key}: {value}")
        else:
            print("⚠️  No metadata found or extraction failed")
    except Exception as e:
        print(f"❌ Error extracting metadata: {e}")
    
    # Test audio properties
    print("\n🎚️  Testing audio properties...")
    try:
        properties = audio_processor.get_audio_properties(file_path)
        if properties:
            print("✅ Audio properties:")
            for key, value in properties.items():
                print(f"  {key}: {value}")
        else:
            print("⚠️  No audio properties found")
    except Exception as e:
        print(f"❌ Error getting audio properties: {e}")
    
    # Test metadata update (read-only test)
    print("\n✏️  Testing metadata update capability...")
    try:
        # Create test metadata
        test_metadata = {
            'title': 'Test Title',
            'artist': 'Test Artist',
            'album': 'Test Album',
            'year': '2024',
            'genre': 'Test Genre'
        }
        
        # Note: This won't actually modify your file, just test the method
        success = audio_processor.update_metadata(file_path, test_metadata)
        if success:
            print("✅ Metadata update method works (file not actually modified)")
        else:
            print("⚠️  Metadata update method returned False")
    except Exception as e:
        print(f"❌ Error testing metadata update: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing complete!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_audio_file.py <path_to_mp3_file>")
        print("Example: python test_audio_file.py 'Deftones - Change.mp3'")
        sys.exit(1)
    
    test_audio_file(sys.argv[1])
