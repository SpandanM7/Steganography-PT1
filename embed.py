# embed.py
import numpy as np
from PIL import Image
import random

def embed_data(image_path, data, output_image_path):
    # Load the image and convert to grayscale
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    
    # Flatten the data into a bitstream (we assume each character is 8 bits)
    bitstream = ''.join(format(byte, '08b') for byte in data.encode())
    
    # Embed the length of the bitstream in the first 32 pixels (32 bits for length)
    bitstream_length = len(bitstream)
    length_bits = format(bitstream_length, '032b')
    
    # Combine length and data bits
    full_bitstream = length_bits + bitstream
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Modify random pixels to embed the data (Patchwork method)
    height, width = img_array.shape
    bits_index = 0
    
    for i in range(height):
        for j in range(width):
            if bits_index < len(full_bitstream):
                # Set the LSB to the bitstream value
                img_array[i, j] = (img_array[i, j] & 254) | int(full_bitstream[bits_index])
                bits_index += 1
            else:
                break

    # Save the modified image
    modified_image = Image.fromarray(img_array)
    modified_image.save(output_image_path)
    print(f"Data embedded and saved in {output_image_path}")

if __name__ == "__main__":
    image_path = 'cover_image.png'  # Path to the cover image
    data = input("Enter data: ")  # Text to embed
    output_image_path = 'stego_image.png'  # Path to save the stego image
    embed_data(image_path, data, output_image_path)