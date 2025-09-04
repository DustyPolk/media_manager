# 🧪 Media File Manager - Testing Guide

This guide explains how to test the Media File Manager on your MP3 files, including the Deftones song you mentioned.

## 🚀 **Quick Start Testing**

### **Option 1: Simple Demo (No MP3 Required)**
```bash
python test_audio_simple.py
```
This shows a demo of the system without requiring any files.

### **Option 2: Interactive Testing**
```bash
python interactive_test.py
```
This provides an interactive menu to test different features with your MP3 files.

### **Option 3: Direct File Testing**
```bash
python test_audio_simple.py "path/to/your/deftones_song.mp3"
```

## 📁 **Test Scripts Available**

| Script | Purpose | Best For |
|--------|---------|----------|
| `test_audio_simple.py` | Simple testing without dependencies | Quick tests, avoiding Windows issues |
| `interactive_test.py` | Interactive testing with menu | Exploring features step by step |
| `test_audio_file.py` | Full testing (may have dependency issues) | Complete testing when all dependencies work |

## 🎵 **Testing Your Deftones Song**

### **Step 1: Locate Your MP3 File**
First, find where your Deftones song is located. You can:
- Use Windows Explorer to find the file
- Note the full path (e.g., `C:\Users\Dustin\Music\Deftones - Change.mp3`)

### **Step 2: Test the File**
```bash
# Replace with your actual file path
python test_audio_simple.py "C:\Users\Dustin\Music\Deftones - Change.mp3"
```

### **Step 3: What to Expect**
The script will test:
- ✅ **Metadata extraction** (title, artist, album, year, genre, etc.)
- ✅ **Audio properties** (duration, bitrate, sample rate, channels)
- ✅ **Metadata handler** (unified interface)
- ✅ **Update capability** (read-only test, won't modify your file)

## 🔍 **What Gets Extracted**

### **Common Metadata Fields**
- **Title** (from ID3 TIT2 tag)
- **Artist** (from ID3 TPE1 tag)
- **Album** (from ID3 TALB tag)
- **Year** (from ID3 TDRC tag)
- **Genre** (from ID3 TCON tag)
- **Track Number** (from ID3 TRCK tag)

### **Technical Properties**
- **Duration** (in seconds)
- **Bitrate** (kbps)
- **Sample Rate** (Hz)
- **Channels** (mono/stereo)
- **Bits per Sample** (for lossless formats)

### **Artwork** (if present)
- **Cover image data**
- **Image format** (JPEG, PNG, etc.)
- **Image dimensions**
- **Color mode**

## 🛠️ **Troubleshooting**

### **File Not Found Error**
- Make sure the file path is correct
- Use quotes around paths with spaces
- Try using forward slashes or escaped backslashes

### **No Metadata Found**
- The MP3 might not have embedded metadata
- Try a different MP3 file with known metadata
- Check if the file is actually an MP3

### **Import Errors**
- Make sure you're in the `media_file_manager` directory
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## 📋 **Example Test Output**

```
🎵 Testing Media File Manager on: Deftones - Change.mp3
==================================================
📋 Testing metadata extraction...
✅ Successfully extracted metadata:
  title: Change (In The House Of Flies)
  artist: Deftones
  album: White Pony
  year: 2000
  genre: Alternative Metal
  track: 4

🎚️  Testing audio properties...
✅ Audio properties:
  duration: 299.0
  bitrate: 320000

🔧 Testing metadata handler...
✅ Metadata handler extracted metadata successfully
   Found 6 metadata fields

✏️  Testing metadata update capability...
✅ Metadata update method works (file not actually modified)
==================================================
🎉 Testing complete!
```

## 🎯 **Next Steps**

Once you've confirmed everything works with your Deftones song:

1. **Test with other MP3 files** to ensure consistency
2. **Try different audio formats** (FLAC, OGG, etc.)
3. **Explore the interactive testing** to understand all features
4. **Check the test coverage** to see what's working

## 🆘 **Need Help?**

If you encounter issues:
1. Check the error messages carefully
2. Verify your file path is correct
3. Ensure you're in the right directory
4. Try the interactive test for step-by-step debugging

Happy testing! 🎵✨
