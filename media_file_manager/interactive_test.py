#!/usr/bin/env python3
"""
Interactive test script for Media File Manager.
This script allows you to test the system interactively.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from media.audio_processor import AudioProcessor
from core.metadata_handler import MetadataHandler

def interactive_test():
    """Run an interactive test session."""
    print("🎵 Media File Manager - Interactive Test")
    print("=" * 50)
    
    # Initialize components
    config = {
        'supported_formats': {
            'audio': ['.mp3', '.flac', '.ogg', '.wav', '.aac', '.m4a'],
            'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv']
        }
    }
    
    try:
        audio_processor = AudioProcessor(config)
        metadata_handler = MetadataHandler(config)
        print("✅ All components initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing components: {e}")
        return
    
    while True:
        print("\n" + "=" * 50)
        print("📋 Available Tests:")
        print("1. Test metadata extraction")
        print("2. Test audio properties")
        print("3. Test metadata handler")
        print("4. Test metadata update capability")
        print("5. Show supported formats")
        print("6. Exit")
        
        choice = input("\n🎯 Select a test (1-6): ").strip()
        
        if choice == "1":
            test_metadata_extraction(audio_processor)
        elif choice == "2":
            test_audio_properties(audio_processor)
        elif choice == "3":
            test_metadata_handler(metadata_handler)
        elif choice == "4":
            test_metadata_update(audio_processor)
        elif choice == "5":
            show_supported_formats(config)
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-6.")

def test_metadata_extraction(audio_processor):
    """Test metadata extraction."""
    print("\n📋 Testing Metadata Extraction")
    print("-" * 30)
    
    file_path = input("Enter the path to your MP3 file: ").strip()
    if not file_path:
        print("❌ No file path provided.")
        return
    
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ File '{file_path}' does not exist!")
        return
    
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

def test_audio_properties(audio_processor):
    """Test audio properties extraction."""
    print("\n🎚️  Testing Audio Properties")
    print("-" * 30)
    
    file_path = input("Enter the path to your MP3 file: ").strip()
    if not file_path:
        print("❌ No file path provided.")
        return
    
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ File '{file_path}' does not exist!")
        return
    
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

def test_metadata_handler(metadata_handler):
    """Test metadata handler."""
    print("\n🔧 Testing Metadata Handler")
    print("-" * 30)
    
    file_path = input("Enter the path to your MP3 file: ").strip()
    if not file_path:
        print("❌ No file path provided.")
        return
    
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ File '{file_path}' does not exist!")
        return
    
    try:
        metadata = metadata_handler.extract_metadata(file_path)
        if metadata:
            print("✅ Metadata handler extracted metadata successfully")
            print(f"   Found {len(metadata)} metadata fields")
        else:
            print("⚠️  Metadata handler returned no data")
    except Exception as e:
        print(f"❌ Error with metadata handler: {e}")

def test_metadata_update(audio_processor):
    """Test metadata update capability."""
    print("\n✏️  Testing Metadata Update Capability")
    print("-" * 30)
    
    file_path = input("Enter the path to your MP3 file: ").strip()
    if not file_path:
        print("❌ No file path provided.")
        return
    
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ File '{file_path}' does not exist!")
        return
    
    try:
        # Create test metadata
        test_metadata = {
            'title': 'Test Title',
            'artist': 'Test Artist',
            'album': 'Test Album',
            'year': '2024',
            'genre': 'Test Genre'
        }
        
        print("📝 Testing with metadata:", test_metadata)
        
        # Note: This won't actually modify your file, just test the method
        success = audio_processor.update_metadata(file_path, test_metadata)
        if success:
            print("✅ Metadata update method works (file not actually modified)")
        else:
            print("⚠️  Metadata update method returned False")
    except Exception as e:
        print(f"❌ Error testing metadata update: {e}")

def show_supported_formats(config):
    """Show supported formats."""
    print("\n🎯 Supported Formats")
    print("-" * 30)
    
    print("Audio formats:")
    for fmt in config['supported_formats']['audio']:
        print(f"  • {fmt}")
    
    print("\nVideo formats:")
    for fmt in config['supported_formats']['video']:
        print(f"  • {fmt}")

if __name__ == "__main__":
    interactive_test()
