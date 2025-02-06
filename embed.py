import numpy as np
from PIL import Image
import random

def embed_data(image_path, data, output_image_path):
    # Load the image
    img = Image.open(image_path).convert('L')
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
                    img_array[i, j] = img_array[i, j] & 254  # Set the LSB to 0
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
data = "hello"
output_image_path = 'stego_image.png'
embed_data(image_path, data, output_image_path)




################################

import numpy as np
from PIL import Image

def retrieve_data(image_path):
    img = Image.open(image_path)
    img_array = np.array(img, dtype=np.uint8)

    extracted_bits = []

    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            pixel_value = img_array[i, j]  # This is either a scalar (grayscale) or an array (RGB)

            if len(img_array.shape) == 2:  # Grayscale
                bit = pixel_value & 1  # Get LSB directly
            else:  # RGB
                bit = pixel_value[0] & 1  # Get LSB from Red channel

            extracted_bits.append(str(bit))

    return ''.join(extracted_bits)

# Example usage
image_path = "stego_image.png"
data = retrieve_data(image_path)
print("Extracted Binary Data:", data)

