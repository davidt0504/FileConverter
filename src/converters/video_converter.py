import os
from moviepy.editor import VideoFileClip


def convert_video(input_file, output_format, keep_both=False):
    """
    Convert video to a different format.
    
    Parameters:
        input_file (str): Path to the input video file.
        output_format (str): The format to convert the video to.
        keep_both (bool): Whether to keep both the original and converted files. If False, the original file is replaced.
    
    Returns:
        str: Path to the converted video file.
    """
    
    # Check if output format is supported
    supported_formats = ['mp4', 'avi', 'mkv', 'flv', 'mov']
    if output_format.lower() not in supported_formats:
        raise ValueError(f"Unsupported output format: {output_format}. Supported formats are {supported_formats}.")
    
    # Generate output file path
    input_filename, input_extension = os.path.splitext(input_file)
    output_file = f"{input_filename}.{output_format.lower()}"
    
    # Check for file existence and append numerical suffix if keep_both is True
    if keep_both and os.path.exists(output_file):
        counter = 1
        while os.path.exists(f"{input_filename}_{counter}.{output_format.lower()}"):
            counter += 1
        output_file = f"{input_filename}_{counter}.{output_format.lower()}"
    
    # Perform video conversion
    with VideoFileClip(input_file) as clip:
        clip.write_videofile(output_file, codec="libx264")  # Using codec="libx264" for now, can be made customizable
        
    return output_file
