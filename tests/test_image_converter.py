import unittest
import os
import tempfile
import shutil
from PIL import Image
from src.converters.image_converter import convert_image

class TestImageConverter(unittest.TestCase):

    def setUp(self):
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()

        # Supported Image Formats
        self.image_formats = ['jpg', 'png', 'gif']

        # Copy sample files to temporary directory
        self.sample_files_dir = os.path.join(os.path.dirname(__file__), 'sample_files')
        for img_format in self.image_formats:
            img_dir = os.path.join(self.sample_files_dir, img_format)
            if os.path.exists(img_dir):
                for filename in os.listdir(img_dir):
                    if filename.endswith(f".{img_format}"):
                        input_file = os.path.join(img_dir, filename)
                        shutil.copy(input_file, self.temp_dir)
            else:
                print(f"Warning: Sample files directory for {img_format} not found: {img_dir}")

    def tearDown(self):
        # Remove temporary directory
        shutil.rmtree(self.temp_dir)

    def test_image_conversion(self):
        for img_format in self.image_formats:
            for filename in os.listdir(self.temp_dir):
                if filename.endswith(f".{img_format}"):
                    input_file = os.path.join(self.temp_dir, filename)
                    output_format = 'png' if img_format != 'png' else 'jpg'
                    
                    # Act
                    convert_image(input_file, output_format)
                    
                    # Assert
                    output_file = f"{os.path.splitext(input_file)[0]}.{output_format}"
                    self.assertTrue(os.path.exists(output_file))
                    with Image.open(output_file) as img:
                        self.assertEqual(img.format, output_format.upper())

    def test_invalid_file_format(self):
        for img_format in self.image_formats:
            for filename in os.listdir(self.temp_dir):
                if filename.endswith(f".{img_format}"):
                    input_file = os.path.join(self.temp_dir, filename)
                    
                    # Act & Assert
                    with self.assertRaises(ValueError):
                        convert_image(input_file, 'invalid_format')

    def test_output_filename(self):
        for img_format in self.image_formats:
            for filename in os.listdir(self.temp_dir):
                if filename.endswith(f".{img_format}"):
                    input_file = os.path.join(self.temp_dir, filename)
                    output_format = 'png' if img_format != 'png' else 'jpg'
                    
                    # Act
                    convert_image(input_file, output_format)
                    
                    # Assert
                    expected_output_filename = f"{os.path.splitext(filename)[0]}.{output_format}"
                    self.assertTrue(os.path.exists(os.path.join(self.temp_dir, expected_output_filename)))

    def test_suffix_appending(self):
        for img_format in self.image_formats:
            for filename in os.listdir(self.temp_dir):
                if filename.endswith(f".{img_format}"):
                    input_file = os.path.join(self.temp_dir, filename)
                    output_format = 'png' if img_format != 'png' else 'jpg'
                    
                    # Act
                    convert_image(input_file, output_format, keep_both=True)
                    
                    # Assert
                    expected_output_filename = f"{os.path.splitext(filename)[0]}_1.{output_format}"
                    self.assertTrue(os.path.exists(os.path.join(self.temp_dir, expected_output_filename)))

if __name__ == '__main__':
    unittest.main()
    