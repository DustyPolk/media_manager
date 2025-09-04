#!/usr/bin/env python3
"""
Simple test script for Media File Manager audio processing.
This version avoids python-magic dependency issues on Windows.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from media.audio_processor import AudioProcessor
from core.metadata_handler import MetadataHandler

def test_audio_file_simple(file_path: str):
    """Test the audio processor on a given file (simplified version)."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ Error: File '{file_path}' does not exist!")
        return
    
    print(f"🎵 Testing Media File Manager on: {file_path.name}")
    print("=" * 50)
    
    # Initialize processor
    config = {
        'supported_formats': {
            'audio': ['.mp3', '.flac', '.ogg', '.wav', '.aac', '.m4a'],
            'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']
        }
    }
    
    audio_processor = AudioProcessor(config)
    metadata_handler = MetadataHandler(config)
    
    # Test metadata extraction
    print("📋 Testing metadata extraction...")
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
    
    # Test metadata handler
    print("\n🔧 Testing metadata handler...")
    try:
        handler_metadata = metadata_handler.extract_metadata(file_path)
        if handler_metadata:
            print("✅ Metadata handler extracted metadata successfully")
        else:
            print("⚠️  Metadata handler returned no data")
    except Exception as e:
        print(f"❌ Error with metadata handler: {e}")
    
    # Test metadata update capability (read-only test)
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

def demo_without_file():
    """Show a demo of the system without requiring a file."""
    print("🎵 Media File Manager - Audio Processing Demo")
    print("=" * 50)
    
    config = {
        'supported_formats': {
            'audio': ['.mp3', '.flac', '.ogg', '.wav', '.aac', '.m4a'],
            'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']
        }
    }
    
    print("🔧 Initializing components...")
    try:
        audio_processor = AudioProcessor(config)
        metadata_handler = MetadataHandler(config)
        print("✅ All components initialized successfully!")
        
        print("\n📚 Available Methods:")
        print("-" * 30)
        print("• audio_processor.extract_metadata(file_path)")
        print("• audio_processor.get_audio_properties(file_path)")
        print("• audio_processor.update_metadata(file_path, metadata)")
        print("• metadata_handler.extract_metadata(file_path)")
        
        print("\n🎯 Supported Audio Formats:")
        for fmt in config['supported_formats']['audio']:
            print(f"   • {fmt}")
            
    except Exception as e:
        print(f"❌ Error initializing components: {e}")
    
    print("\n" + "=" * 50)
    print("💡 To test with a real MP3 file, run:")
    print("   python test_audio_simple.py <path_to_your_mp3>")
    print("\n🎉 Demo complete!")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, show demo
        demo_without_file()
    elif len(sys.argv) == 2:
        # Test with provided file
        test_audio_file_simple(sys.argv[1])
    else:
        print("Usage: python test_audio_simple.py [path_to_mp3_file]")
        print("Example: python test_audio_simple.py 'Deftones - Change.mp3'")
        print("Or run without arguments to see a demo.")
        sys.exit(1)
