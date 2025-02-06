import numpy as np
from PIL import Image

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

if __name__ == "__main__":
    image_path = "stego_image.png"  # Path to the stego image
    extracted_text = retrieve_data(image_path)
    print("Extracted Text:", extracted_text)