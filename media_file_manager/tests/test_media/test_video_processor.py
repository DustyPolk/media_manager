
import unittest
from pathlib import Path
from media.video_processor import VideoProcessor

class TestVideoProcessor(unittest.TestCase):
    def setUp(self):
        self.config = {}
        self.processor = VideoProcessor(self.config)
        self.test_file = Path("test.mp4")

    def test_extract_metadata(self):
        metadata = self.processor.extract_metadata(self.test_file)
        self.assertEqual(metadata, {})

    def test_update_metadata(self):
        success = self.processor.update_metadata(self.test_file, {})
        self.assertFalse(success)

if __name__ == '__main__':
    unittest.main()
