# Created: December 18, 2024
# Author: Kevin Puklicz
# Input: Bounding Box Length

# Define the range and spacing for the section cut
length = get_measurement(0)
lengthv = length.value
start = -0.5 * lengthv
end = 0.5 * lengthv - 5
spacing = 1

# Calculate the number of elements in the array based on the range and spacing
num_elements = int((end - start) / spacing) + 1

# Create the array of evenly spaced values
Y = numpy.linspace(start, end, num_elements)

# Send the generated array as output
outputs.send_measurement(0, Y)