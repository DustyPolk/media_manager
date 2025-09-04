import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from media.audio_processor import AudioProcessor

class TestAudioProcessor(unittest.TestCase):
    def setUp(self):
        self.config = {
            'supported_formats': {
                'audio': ['.mp3', '.flac', '.ogg']
            }
        }
        self.processor = AudioProcessor(self.config)

    @patch('mutagen.File')
    def test_extract_metadata_mp3(self, mock_mutagen_file):
        # Create a mock audio file object
        mock_audio = MagicMock()
        mock_audio.tags = {
            'TIT2': ['Test Title'],
            'TPE1': ['Test Artist'],
            'TALB': ['Test Album'],
            'TDRC': ['2023'],
            'TCON': ['Pop'],
            'TRCK': ['1'],
        }
        mock_audio.info.length = 300
        mock_audio.info.bitrate = 320000
        mock_mutagen_file.return_value = mock_audio

        # Call the method under test
        metadata = self.processor.extract_metadata(Path('test.mp3'))

        # Assert the results
        self.assertEqual(metadata['title'], 'Test Title')
        self.assertEqual(metadata['artist'], 'Test Artist')
        self.assertEqual(metadata['album'], 'Test Album')
        self.assertEqual(metadata['year'], '2023')
        self.assertEqual(metadata['genre'], 'Pop')
        self.assertEqual(metadata['track'], '1')
        self.assertEqual(metadata['duration'], 300)
        self.assertEqual(metadata['bitrate'], 320000)

    @patch('mutagen.File')
    def test_update_metadata_mp3(self, mock_mutagen_file):
        # Create a mock audio file object with proper tag handling
        mock_audio = MagicMock()
        # Create a real dictionary for tags
        tags_dict = {}
        mock_audio.tags = tags_dict
        mock_mutagen_file.return_value = mock_audio

        # Create metadata to update
        metadata = {
            'title': 'New Title',
            'artist': 'New Artist',
            'album': 'New Album',
            'year': '2024',
            'genre': 'Rock',
            'track': '2',
        }

        # Call the method under test
        success = self.processor.update_metadata(Path('test.mp3'), metadata)

        # Assert the results
        self.assertTrue(success)
        mock_audio.save.assert_called_once()
        # Check that the tags were actually assigned
        self.assertEqual(tags_dict['TIT2'], 'New Title')
        self.assertEqual(tags_dict['TPE1'], 'New Artist')
        self.assertEqual(tags_dict['TALB'], 'New Album')
        self.assertEqual(tags_dict['TDRC'], '2024')
        self.assertEqual(tags_dict['TCON'], 'Rock')
        self.assertEqual(tags_dict['TRCK'], '2')

    @patch('mutagen.File')
    def test_extract_artwork(self, mock_mutagen_file):
        # Create a mock audio file object with artwork
        mock_audio = MagicMock()
        mock_artwork_data = b'artwork_data'
        mock_apic = MagicMock()
        mock_apic.data = mock_artwork_data
        mock_audio.tags = {'APIC:': mock_apic}
        mock_mutagen_file.return_value = mock_audio

        # Mock Image.open
        with patch('PIL.Image.open') as mock_image_open:
            mock_image = MagicMock()
            mock_image.format = 'jpeg'
            mock_image.size = (100, 100)
            mock_image.mode = 'RGB'
            mock_image_open.return_value = mock_image

            # Call the method under test
            artwork = self.processor._extract_artwork(mock_audio)

            # Assert the results
            self.assertIsNotNone(artwork)
            self.assertEqual(artwork['data'], mock_artwork_data)
            self.assertEqual(artwork['format'], 'jpeg')
            self.assertEqual(artwork['size'], (100, 100))
            self.assertEqual(artwork['mode'], 'RGB')

if __name__ == '__main__':
    unittest.main()