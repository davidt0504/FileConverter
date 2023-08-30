import argparse
from src.converters.image_converter import convert_image
from src.converters.video_converter import convert_video
from src.gui import FileConverterGUI
from tkinter import Tk

def main():
    parser = argparse.ArgumentParser(description="File Converter")
    parser.add_argument("-g", "--gui", help="Launch GUI", action="store_true")
    parser.add_argument("-f", "--file", help="File to convert")
    parser.add_argument("-t", "--type", help="Output file type")
    parser.add_argument("-s", "--subdirs", help="Scan subdirectories", action="store_true")

    args = parser.parse_args()

    if args.gui:
        root = Tk()
        app = FileConverterGUI(root)
        root.mainloop()
    else:
        file_path = args.file
        output_type = args.type
        scan_subdirs = args.subdirs

        if not file_path or not output_type:
            print("Both file and type are required for CLI mode.")
            return

        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            convert_image(file_path, output_type)
        elif file_path.lower().endswith(('.mp4', '.flv', '.mkv', '.3gp', '.mpg')):
            convert_video(file_path, output_type)
        else:
            print("Invalid file type.")

if __name__ == "__main__":
    main()
