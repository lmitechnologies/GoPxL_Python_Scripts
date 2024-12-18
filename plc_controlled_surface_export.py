#Created: Decemebr 18 2024
#Author: Kevin Puklicz
#Input 1: Uniform Surface
#System Arc: PC Instance 

#This code reads an enable bit and a string value from an AB PLC
# If the enable bit is low, it skips the entire script and sends an output value of 3.
# If the enable bit is high, it reads the string value and uses it to name a saved PNG file.
# It then saves a surface as a PNG image using this file path.
# If successful, it updates a test bit on the PLC to indicate that the string was read successfully.
# The code also sends a success or failure output to indicate the result of the operation.


import numpy as np
from datetime import datetime
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap
from pycomm3 import LogixDriver

# Define the IP address of the PLC
plc_ip = '192.168.1.88'

# Define the tag you want to read
bit_tag_name = 'LMI_Acknowledge_Bit'  # Replace with the actual tag name
string_tag_name = 'LMI_Name_String'
enable_bit_tag_name = 'LMI_Enable_Bit'  # Replace with the actual enable bit tag name
bit_index = 0  # Replace with the actual bit index you want to read

# Main function
def main():
    # Read the enable bit from the PLC
    enable_bit = read_enable_bit(plc_ip, enable_bit_tag_name)
    
    # If the enable bit is low, skip the entire script and send output value of 3
    if enable_bit == 0:
        outputs.send_measurement(0, 3)
        return

    # Read the string value from the PLC
    string_value = read_plc(plc_ip, bit_tag_name, string_tag_name)
    
    # If the string value is None, send a failure output and exit
    if string_value is None:
        outputs.send_measurement(0, 0)  # Send failure output
        return

    # Use the string to name the saved PNG file
    image_file_path = rf'C:\GoTools\DataExport\images\{string_value}.png'

    # Save the surface as a PNG
    surface = get_surface(0)
    save_surface_as_png(surface, image_file_path)

    # If successful, update test bit to show we read the string
    try:
        with LogixDriver(plc_ip) as plc:
            plc.write((bit_tag_name, 1))  # Change the test bit to 1
            result = plc.read(bit_tag_name)
            log_info(result.value)
        outputs.send_measurement(0, 1)  # Send success output
    except Exception as e:
        log_info(f"Error updating test bit: {e}")
        outputs.send_measurement(0, 0)  # Send failure output

# Function to read the PLC
def read_plc(plc_ip, bit_tag_name, string_tag_name):
    try:
        # Connect to the PLC
        with LogixDriver(plc_ip) as plc:
            # Check string status
            result = plc.read(bit_tag_name)
            log_info(result.value)

            # Read string
            var = plc.read(string_tag_name)
            log_info(var)

            return var.value
    except Exception as e:
        log_info(f"Error reading PLC: {e}")
        return None

# Function to read the enable bit from the PLC
def read_enable_bit(plc_ip, enable_bit_tag_name):
    try:
        # Connect to the PLC
        with LogixDriver(plc_ip) as plc:
            # Read the enable bit
            result = plc.read(enable_bit_tag_name)
            log_info(result.value)
            return result.value
    except Exception as e:
        log_info(f"Error reading enable bit from PLC: {e}")
        return None

# Function to save the surface as a PNG
def save_surface_as_png(surface, file_path):
    try:
        # Extract scale and calculate aspect ratio
        scale = np.array([surface.scale.x, surface.scale.y, surface.scale.z])
        
        # Check for division by zero
        if scale[0] == 0:
            log_info("Error calculating aspect ratio: division by zero")
            return

        aspect_ratio = scale[1] / scale[0] # divide height width

        # Adjust z relative to a baseline of 0
        adjusted_points = surface.points - surface.offset.z

        # Normalize z values between 0 and 1
        normalized_points = (adjusted_points - adjusted_points.min()) / (adjusted_points.max() - adjusted_points.min())

        # Define the custom colormap with transparency
        colors = LinearSegmentedColormap.from_list("my_palette_with_alpha",
            [
                (0.0, (0.0, 0.0, 0.0, 0.0)), # Position 0.0, RGBA black with 0% opacit)
                (0.2, (0.25, 0.25, 1.0, 1.0)),
                (0.4, (0.2, 0.8, 0.2, 1.0)),
                (0.6, (1.0, 0.84, 0.0, 1.0)),
                (0.8, (1.0, 0.27, 0.0, 1.0)), 
                (1.0, (1.0, 1.0, 1.0, 1.0)), 
            ],
        )

        colormap = colors(normalized_points)
        rgba_image = (colormap * 255).astype(np.uint8) # Scale from 0 to 1 to 8-bit depth (0-255)

        # Keep aspect ratio
        height, width = normalized_points.shape
        height = int(height * aspect_ratio)
        img = Image.fromarray(rgba_image, mode="RGBA") # Some other options L (grayscale, 8-bit), RGBA, CMYK, YCbCr, I (32-bit signed integer), LA (grayscale with alpha),
        img = img.resize((width, height), Image.Resampling.LANCZOS) # Resampling filter - other options Image.Resampling.NEAREST, Image.Resampling.BICUBIC

        img.save(file_path, "PNG")
    except Exception as e:
        log_info(f"Error saving image: {e}")

main()
