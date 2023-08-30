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
        self.video_formats = ['mp4', 'flv', 'mkv', '3gp']

        # Copy sample files to temporary directory
        self.sample_files_dir = os.path.join(os.path.dirname(__file__), 'sample_files')
        for video_format in self.video_formats:
            video_dir = os.path.join(self.sample_files_dir, video_format)
            if os.path.exists(video_dir):
                for filename in os.listdir(video_dir):
                    if filename.endswith(f".{video_format}"):
                        input_file = os.path.join(video_dir, filename)
                        shutil.copy(input_file, self.temp_dir)
            else:
                print(f"Warning: Sample files directory for {video_format} not found: {video_dir}")

    def tearDown(self):
        # Remove temporary directory
        shutil.rmtree(self.temp_dir)

    def test_video_conversion(self):
        for video_format in self.video_formats:
            for filename in os.listdir(self.temp_dir):
                if filename.endswith(f".{video_format}"):
                    input_file = os.path.join(self.temp_dir, filename)
                    output_format = 'mp4' if video_format != 'mp4' else 'flv'
                    
                    # Act
                    convert_video(input_file, output_format)
                    
                    # Assert
                    output_file = f"{os.path.splitext(input_file)[0]}.{output_format}"
                    self.assertTrue(os.path.exists(output_file))

                    with VideoFileClip(output_file) as clip:
                        self.assertEqual(clip.fps, 24)

    def test_invalid_file_format(self):
        for video_format in self.video_formats:
            for filename in os.listdir(self.temp_dir):
                if filename.endswith(f".{video_format}"):
                    input_file = os.path.join(self.temp_dir, filename)
                    
                    # Act & Assert
                    with self.assertRaises(ValueError):
                        convert_video(input_file, 'invalid_format')

    def test_output_filename(self):
        for video_format in self.video_formats:
            for filename in os.listdir(self.temp_dir):
                if filename.endswith(f".{video_format}"):
                    input_file = os.path.join(self.temp_dir, filename)
                    output_format = 'mp4' if video_format != 'mp4' else 'flv'
                    
                    # Act
                    convert_video(input_file, output_format)
                    
                    # Assert
                    expected_output_filename = f"{os.path.splitext(filename)[0]}.{output_format}"
                    self.assertTrue(os.path.exists(os.path.join(self.temp_dir, expected_output_filename)))

    def test_suffix_appending(self):
        for video_format in self.video_formats:
            for filename in os.listdir(self.temp_dir):
                if filename.endswith(f".{video_format}"):
                    input_file = os.path.join(self.temp_dir, filename)
                    output_format = 'mp4' if video_format != 'mp4' else 'flv'
                    
                    # Act
                    convert_video(input_file, output_format, keep_both=True)
                    
                    # Assert
                    expected_output_filename = f"{os.path.splitext(filename)[0]}_1.{output_format}"
                    self.assertTrue(os.path.exists(os.path.join(self.temp_dir, expected_output_filename)))

if __name__ == '__main__':
    unittest.main()

