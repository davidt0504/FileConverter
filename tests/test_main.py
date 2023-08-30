import unittest
from unittest.mock import patch, MagicMock
from src import main

class TestMain(unittest.TestCase):

    @patch('src.main.FileConverterGUI')
    def test_gui_launch(self, MockGUI):
        """
        Test that the GUI launches correctly with the -g flag.
        """
        test_args = ["main.py", "-g"]
        with patch.object(main, "__name__", "__main__"):
            with patch.object(main, "exit"):
                with patch.object(main.sys, 'argv', test_args):
                    main.main()
        MockGUI.assert_called_once()

    @patch('src.main.convert_image')
    def test_cli_image_conversion(self, MockConvertImage):
        """
        Test that image conversion works from the CLI.
        """
        test_args = ["main.py", "-f", "somefile.jpg", "-t", "png"]
        with patch.object(main.sys, 'argv', test_args):
            main.main()
        MockConvertImage.assert_called_once_with("somefile.jpg", "png")

    @patch('src.main.convert_video')
    def test_cli_video_conversion(self, MockConvertVideo):
        """
        Test that video conversion works from the CLI.
        """
        test_args = ["main.py", "-f", "somefile.mp4", "-t", "flv"]
        with patch.object(main.sys, 'argv', test_args):
            main.main()
        MockConvertVideo.assert_called_once_with("somefile.mp4", "flv")

    def test_missing_args(self):
        """
        Test that an error is shown when necessary arguments are not provided.
        """
        test_args = ["main.py", "-f", "somefile.jpg"]
        with patch.object(main.sys, 'argv', test_args):
            with patch('builtins.print') as mocked_print:
                main.main()
        mocked_print.assert_called_with("Both file and type are required for CLI mode.")

if __name__ == "__main__":
    unittest.main()
