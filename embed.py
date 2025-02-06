import numpy as np
from PIL import Image
import random

def embed_data(image_path, data, output_image_path):
    # Load the image
    img = Image.open(image_path)
    img_array = np.array(img)
    #print(img_array.shape)
    # Flatten the data into a bitstream (we assume each character is 8 bits)
    bitstream = ''.join(format(byte, '08b') for byte in data.encode())
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Modify random pixels to embed the data (Patchwork method)
    height, width = img_array.shape[:2]
    bits_index = 0
    for i in range(height):
        for j in range(width):
            if bits_index < len(bitstream):
                # Randomly modify pixel
                if random.random() > 0.5:
                    img_array[i, j] = img_array[i, j] & ~1  # Set the LSB to 0
                    img_array[i, j] = img_array[i, j] | int(bitstream[bits_index])  # Set the LSB to the bitstream value
                    bits_index += 1
            if bits_index >= len(bitstream):
                break

    # Save the modified image
    modified_image = Image.fromarray(img_array)
    modified_image.save(output_image_path)
    print(f"Data embedded and saved in {output_image_path}")

# Example usage
image_path = 'cover_image.png'
data = "Secret Message"
output_image_path = 'stego_image.png'
embed_data(image_path, data, output_image_path)




################################

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
