import numpy as np
from PIL import Image
import random

def extract_data(stego_image_path, data_length):
    # Load the stego image
    img = Image.open(stego_image_path)
    img_array = np.array(img)
    
    # Flatten the image pixels and extract the LSB bits
    height, width = img_array.shape[:2]
    bitstream = []
    random.seed(42)
    
    for i in range(height):
        for j in range(width):
            if len(bitstream) < data_length * 8:  # Each character is 8 bits
                pixel_value = img_array[i, j]
                bit = pixel_value[0] & 1  # Get the LSB of the red channel
                bitstream.append(str(bit))
            if len(bitstream) >= data_length * 8:
                break

    # Convert the bitstream back to bytes
    byte_data = []
    for i in range(0, len(bitstream), 8):
        byte_data.append(int(''.join(bitstream[i:i+8]), 2))
    
    # Decode the bytes to a string
    decoded_data = bytes(byte_data).decode('utf-8', errors='ignore')
    return decoded_data

# Example usage
stego_image_path = 'stego_image.png'
retrieved_data = extract_data(stego_image_path, len(data))
print(f"Retrieved Data: {retrieved_data}")
