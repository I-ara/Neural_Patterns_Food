import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('yourimagename.png')

# Convert the image from BGR to RGBA (for transparency support)
image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

# Set a threshold for darkness, adjust this value to reduce the amount of dark removed
threshold = 0.5

# Create a mask for pixels that are close to black (dark pixels)
dark_pixels = (image_rgba[:, :, 0] < threshold) & (image_rgba[:, :, 1] < threshold) & (image_rgba[:, :, 2] < threshold)

# Set alpha (transparency) channel to 0 for dark pixels (making them transparent)
image_rgba[dark_pixels, 3] = 0

# Save the image as SVG with transparent background using matplotlib
plt.imshow(cv2.cvtColor(image_rgba, cv2.COLOR_BGRA2RGBA))  # Convert BGR to RGB for display
plt.axis('off')  # Turn off the axis
plt.savefig("output_image.svg", format="svg", transparent=True)

