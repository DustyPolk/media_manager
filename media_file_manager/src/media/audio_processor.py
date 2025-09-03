"""
Audio file processing for Media File Manager.

This module handles audio-specific operations including metadata
extraction, modification, and file processing.
"""

import mutagen
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)


class AudioProcessor:
    """
    Handles audio file processing and metadata operations.
    
    This class provides functionality to extract, modify, and write
    metadata for various audio formats.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize audio processor with configuration.
        
        Args:
            config: Application configuration dictionary
        """
        self.config = config
        self.supported_formats = config.get('supported_formats', {}).get('audio', [])
        
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from audio file.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary containing extracted metadata
        """
        try:
            audio = mutagen.File(file_path)
            if audio is None:
                logger.warning(f"Could not read audio file: {file_path}")
                return {}
                
            metadata = {}
            
            # Extract common metadata fields
            metadata.update(self._extract_common_metadata(audio))
            
            # Extract format-specific metadata
            metadata.update(self._extract_format_metadata(audio, file_path))
            
            # Extract technical information
            metadata.update(self._extract_technical_info(audio, file_path))
            
            # Extract artwork if available
            artwork = self._extract_artwork(audio)
            if artwork:
                metadata['artwork'] = artwork
                
            logger.debug(f"Extracted metadata from {file_path}: {metadata}")
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting metadata from {file_path}: {e}")
            return {}
            
    def update_metadata(self, file_path: Path, metadata: Dict[str, Any]) -> bool:
        """
        Update metadata in audio file.
        
        Args:
            file_path: Path to the audio file
            metadata: Metadata to write
            
        Returns:
            True if metadata was updated successfully
        """
        try:
            audio = mutagen.File(file_path)
            if audio is None:
                logger.error(f"Could not read audio file for metadata update: {file_path}")
                return False
                
            # Update common metadata
            self._update_common_metadata(audio, metadata)
            
            # Update format-specific metadata
            self._update_format_metadata(audio, metadata)
            
            # Update artwork if provided
            if 'artwork' in metadata:
                self._update_artwork(audio, metadata['artwork'])
                
            # Save changes
            audio.save()
            
            logger.info(f"Successfully updated metadata for {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating metadata for {file_path}: {e}")
            return False
            
    def _extract_common_metadata(self, audio: mutagen.File) -> Dict[str, Any]:
        """Extract common metadata fields from audio file."""
        metadata = {}
        
        # Common ID3 tags
        common_tags = {
            'title': ['title', 'TIT2'],
            'artist': ['artist', 'TPE1'],
            'album': ['album', 'TALB'],
            'year': ['year', 'TDRC'],
            'genre': ['genre', 'TCON'],
            'track': ['track', 'TRCK'],
            'comment': ['comment', 'COMM'],
            'composer': ['composer', 'TCOM'],
            'lyrics': ['lyrics', 'USLT'],
        }
        
        for field, tag_names in common_tags.items():
            value = None
            for tag_name in tag_names:
                if hasattr(audio, 'tags') and audio.tags:
                    if tag_name in audio.tags:
                        value = str(audio.tags[tag_name][0])
                        break
                    elif hasattr(audio.tags, 'get') and audio.tags.get(tag_name):
                        value = str(audio.tags.get(tag_name)[0])
                        break
                        
            if value:
                metadata[field] = value
                
        return metadata
        
    def _extract_format_metadata(self, audio: mutagen.File, file_path: Path) -> Dict[str, Any]:
        """Extract format-specific metadata."""
        metadata = {}
        
        # MP3 specific
        if hasattr(audio, 'info') and hasattr(audio.info, 'bitrate'):
            metadata['bitrate'] = audio.info.bitrate
            
        # FLAC specific
        if hasattr(audio, 'info') and hasattr(audio.info, 'sample_rate'):
            metadata['sample_rate'] = audio.info.sample_rate
            metadata['channels'] = audio.info.channels
            metadata['bits_per_sample'] = audio.info.bits_per_sample
            
        # Vorbis comments (OGG, FLAC)
        if hasattr(audio, 'tags') and audio.tags:
            vorbis_tags = ['bpm', 'key', 'mood', 'language']
            for tag in vorbis_tags:
                if tag in audio.tags:
                    metadata[tag] = str(audio.tags[tag][0])
                    
        return metadata
        
    def _extract_technical_info(self, audio: mutagen.File, file_path: Path) -> Dict[str, Any]:
        """Extract technical information about the audio file."""
        info = {}
        
        if hasattr(audio, 'info'):
            if hasattr(audio.info, 'length'):
                info['duration'] = audio.info.length
            if hasattr(audio.info, 'bitrate'):
                info['bitrate'] = audio.info.bitrate
            if hasattr(audio.info, 'sample_rate'):
                info['sample_rate'] = audio.info.sample_rate
            if hasattr(audio.info, 'channels'):
                info['channels'] = audio.info.channels
                
        return info
        
    def _extract_artwork(self, audio: mutagen.File) -> Optional[Dict[str, Any]]:
        """Extract artwork from audio file."""
        try:
            if hasattr(audio, 'tags') and audio.tags:
                # Look for artwork in different tag formats
                artwork_keys = ['APIC:', 'APIC:cover', 'APIC:front', 'covr']
                
                for key in artwork_keys:
                    if key in audio.tags:
                        artwork_data = audio.tags[key]
                        if isinstance(artwork_data, list):
                            artwork_data = artwork_data[0]
                            
                        if hasattr(artwork_data, 'data'):
                            # Convert to PIL Image for processing
                            try:
                                image = Image.open(io.BytesIO(artwork_data.data))
                                return {
                                    'data': artwork_data.data,
                                    'format': image.format,
                                    'size': image.size,
                                    'mode': image.mode
                                }
                            except Exception as e:
                                logger.debug(f"Failed to process artwork: {e}")
                                
            return None
            
        except Exception as e:
            logger.debug(f"Error extracting artwork: {e}")
            return None
            
    def _update_common_metadata(self, audio: mutagen.File, metadata: Dict[str, Any]) -> None:
        """Update common metadata fields in audio file."""
        # Common ID3 tags mapping
        tag_mapping = {
            'title': 'TIT2',
            'artist': 'TPE1',
            'album': 'TALB',
            'year': 'TDRC',
            'genre': 'TCON',
            'track': 'TRCK',
            'comment': 'COMM',
            'composer': 'TCOM',
        }
        
        for field, tag_name in tag_mapping.items():
            if field in metadata and metadata[field]:
                if hasattr(audio, 'tags') and audio.tags:
                    audio.tags[tag_name] = str(metadata[field])
                    
    def _update_format_metadata(self, audio: mutagen.File, metadata: Dict[str, Any]) -> None:
        """Update format-specific metadata."""
        # Vorbis comments for OGG/FLAC
        if hasattr(audio, 'tags') and audio.tags:
            vorbis_fields = ['bpm', 'key', 'mood', 'language']
            for field in vorbis_fields:
                if field in metadata and metadata[field]:
                    audio.tags[field] = [str(metadata[field])]
                    
    def _update_artwork(self, audio: mutagen.File, artwork: Dict[str, Any]) -> None:
        """Update artwork in audio file."""
        try:
            if hasattr(audio, 'tags') and audio.tags:
                # Create APIC frame for ID3 tags
                from mutagen.id3 import APIC
                
                apic = APIC(
                    encoding=3,  # UTF-8
                    mime=artwork.get('format', 'image/jpeg'),
                    type=3,  # Front cover
                    desc='Cover',
                    data=artwork['data']
                )
                
                audio.tags['APIC:cover'] = apic
                
        except Exception as e:
            logger.error(f"Error updating artwork: {e}")
            
    def get_audio_properties(self, file_path: Path) -> Dict[str, Any]:
        """
        Get comprehensive audio properties.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary containing audio properties
        """
        try:
            audio = mutagen.File(file_path)
            if audio is None:
                return {}
                
            properties = {}
            
            if hasattr(audio, 'info'):
                info = audio.info
                
                # Basic properties
                if hasattr(info, 'length'):
                    properties['duration'] = info.length
                if hasattr(info, 'bitrate'):
                    properties['bitrate'] = info.bitrate
                if hasattr(info, 'sample_rate'):
                    properties['sample_rate'] = info.sample_rate
                if hasattr(info, 'channels'):
                    properties['channels'] = info.channels
                if hasattr(info, 'bits_per_sample'):
                    properties['bits_per_sample'] = info.bits_per_sample
                    
            return properties
            
        except Exception as e:
            logger.error(f"Error getting audio properties for {file_path}: {e}")
            return {}
