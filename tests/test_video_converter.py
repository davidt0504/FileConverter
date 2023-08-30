import unittest
import os
import tempfile
import shutil
from moviepy.editor import VideoFileClip
from src.converters.video_converter import convert_video

class TestVideoConverter(unittest.TestCase):

    def setUp(self):
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()

        # Supported Video Formats
        self.video_formats = ['mp4', 'mkv', 'flv', '3gp']

        # Copy sample files to temporary directory
        self.sample_files_dir = os.path.join(os.path.dirname(__file__), 'sample_files')
        for vid_format in self.video_formats:
            vid_dir = os.path.join(self.sample_files_dir, vid_format)
            for filename in os.listdir(vid_dir):
                if filename.endswith(f".{vid_format}"):
                    input_file = os.path.join(vid_dir, filename)
                    shutil.copy(input_file, self.temp_dir)

    def tearDown(self):
        # Remove temporary directory
        shutil.rmtree(self.temp_dir)

    def test_video_conversion(self):
        for vid_format in self.video_formats:
            for filename in os.listdir(self.temp_dir):
                if filename.endswith(f".{vid_format}"):
                    input_file = os.path.join(self.temp_dir, filename)
                    output_format = 'mp4' if vid_format != 'mp4' else 'mkv'
                    
                    # Act
                    convert_video(input_file, output_format)
                    
                    # Assert
                    output_file = f"{os.path.splitext(input_file)[0]}.{output_format}"
                    self.assertTrue(os.path.exists(output_file))
                    with VideoFileClip(output_file) as clip:
                        self.assertTrue(clip.duration > 0)

    def test_invalid_file_format(self):
        for vid_format in self.video_formats:
            self.temp_dir = os.path.join(self.sample_files_dir, vid_format)
            for filename in os.listdir(self.temp_dir):
                if filename.endswith(f".{vid_format}"):
                    input_file = os.path.join(self.temp_dir, filename)
                    
                    # Act & Assert
                    with self.assertRaises(ValueError):
                        convert_video(input_file, 'invalid_format')

    def test_output_filename(self):
        for vid_format in self.video_formats:
            self.temp_dir = os.path.join(self.sample_files_dir, vid_format)
            for filename in os.listdir(self.temp_dir):
                if filename.endswith(f".{vid_format}"):
                    input_file = os.path.join(self.temp_dir, filename)
                    output_format = 'mkv' if vid_format != 'mkv' else 'mp4'
                    
                    # Act
                    convert_video(input_file, output_format)
                    
                    # Assert
                    expected_output_filename = f"{os.path.splitext(filename)[0]}.{output_format}"
                    self.assertTrue(os.path.exists(os.path.join(self.temp_dir, expected_output_filename)))

    def test_suffix_appending(self):
        for vid_format in self.video_formats:
            self.temp_dir = os.path.join(self.sample_files_dir, vid_format)
            for filename in os.listdir(self.temp_dir):
                if filename.endswith(f".{vid_format}"):
                    input_file = os.path.join(self.temp_dir, filename)
                    output_format = 'mkv' if vid_format != 'mkv' else 'mp4'
                    
                    # Act
                    convert_video(input_file, output_format, keep_both=True)
                    
                    # Assert
                    expected_output_filename = f"{os.path.splitext(filename)[0]}_1.{output_format}"
                    self.assertTrue(os.path.exists(os.path.join(self.temp_dir, expected_output_filename)))

if __name__ == '__main__':
    unittest.main()

