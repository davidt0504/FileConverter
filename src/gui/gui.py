import os
import glob
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from src.converters.image_converter import convert_image
from src.converters.video_converter import convert_video

class FileConverterGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("File Converter")
        self.selected_file_path = ""
        self.selected_type = StringVar()
        self.scan_subdirs = BooleanVar()

        # File selection button
        self.btn_select = Button(window, text="Select File/Directory", command=self.select_file)
        self.btn_select.pack()

        # Type selection dropdown
        self.dropdown = OptionMenu(window, self.selected_type, "jpg", "png", "mp4", "mp3")
        self.dropdown.pack()

        # Checkbox for scanning subdirectories
        self.check_subdirs = Checkbutton(window, text="Scan Subdirectories", variable=self.scan_subdirs)
        self.check_subdirs.pack()

        # Conversion button
        self.btn_convert = Button(window, text="Start Conversion", command=self.start_conversion)
        self.btn_convert.pack()

        # Progress bar
        self.progress = Progressbar(window, orient=HORIZONTAL, length=200, mode="determinate")
        self.progress.pack()

        # Progress label
        self.label_progress = Label(window, text="Progress")
        self.label_progress.pack()

    def select_file(self):
        self.selected_file_path = filedialog.askopenfilename()
        if os.path.isdir(self.selected_file_path):
            print("Selected a directory:", self.selected_file_path)
        elif os.path.isfile(self.selected_file_path):
            print("Selected a file:", self.selected_file_path)
        else:
            print("Invalid selection")

    def start_conversion(self):
        file_path = self.selected_file_path
        output_type = self.selected_type.get()
        scan_subdirs = self.scan_subdirs.get()

        if os.path.isdir(file_path):
            all_files = glob.glob(f"{file_path}/*.*")
            if scan_subdirs:
                all_files += glob.glob(f"{file_path}/**/*.*", recursive=True)

            total_files = len(all_files)
            converted_files = 0

            for file in all_files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    convert_image(file, output_type)
                elif file.lower().endswith(('.mp4', '.flv', '.mkv', '.3gp', '.mpg')):
                    convert_video(file, output_type)
                
                converted_files += 1
                progress_percent = (converted_files / total_files) * 100
                self.progress['value'] = progress_percent
                self.label_progress['text'] = f"{progress_percent:.2f}% - {converted_files}/{total_files} files converted"

        elif os.path.isfile(file_path):
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                convert_image(file_path, output_type)
            elif file_path.lower().endswith(('.mp4', '.flv', '.mkv', '.3gp', '.mpg')):
                convert_video(file_path, output_type)
            
            self.progress['value'] = 100
            self.label_progress['text'] = "100% - 1/1 file converted"

        else:
            print("Invalid selection")

if __name__ == "__main__":
    root = Tk()
    app = FileConverterGUI(root)
    root.mainloop()
