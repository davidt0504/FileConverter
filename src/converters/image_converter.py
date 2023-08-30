from PIL import Image
import os


def convert_image(input_file, output_format, keep_both=False):
    """
    Convert image to a different format.
    
    Parameters:
        input_file (str): Path to the input image file.
        output_format (str): The format to convert the image to.
        keep_both (bool): Whether to keep both the original and converted files. If False, the original file is replaced.
    
    Returns:
        str: Path to the converted image file.
    """
    
    # Check if output format is supported
    supported_formats = ['jpg', 'png', 'webp', 'bmp', 'gif', 'tiff']
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
    
    # Perform image conversion
    with Image.open(input_file) as img:
        img.save(output_file, format='JPEG' if output_format.upper() == 'JPG' else output_format.upper())
        
    return output_file
