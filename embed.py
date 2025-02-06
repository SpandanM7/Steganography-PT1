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

def binary_to_text(binary_string):
    """Convert binary string to text (8 bits per character)."""
    chars = [chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8)]
    return ''.join(chars)

def retrieve_data(image_path):
    img = Image.open(image_path).convert('L')
    img_array = np.array(img, dtype=np.uint8)

    extracted_bits = []
    
    # Extract the first 32 bits to get the length of the bitstream
    length_bits = []
    for i in range(32):
        pixel_value = img_array[i // img_array.shape[1], i % img_array.shape[1]]
        bit = pixel_value & 1
        length_bits.append(str(bit))
    
    bitstream_length = int(''.join(length_bits), 2)
    
    # Extract the actual bitstream
    bits_extracted = 0
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            if bits_extracted >= bitstream_length + 32:
                break
            if bits_extracted >= 32:  # Skip the first 32 bits (length)
                pixel_value = img_array[i, j]
                bit = pixel_value & 1
                extracted_bits.append(str(bit))
            bits_extracted += 1

    # Convert bits to text
    binary_string = ''.join(extracted_bits)
    hidden_text = binary_to_text(binary_string)
    
    return hidden_text

# Example usage
image_path = 'cover_image.png'
data = input("Enter your data: ")
output_image_path = 'stego_image.png'
embed_data(image_path, data, output_image_path)

# Retrieve the embedded data
image_path = "stego_image.png"
extracted_text = retrieve_data(image_path)
print("Extracted Text:", extracted_text)