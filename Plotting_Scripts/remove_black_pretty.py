import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('directoryofyourimage.png')

# Convert the image from BGR to RGBA (for transparency support)
image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

# Set a threshold for darkness (tune this value as needed)
threshold = 0.5

# Create a mask for pixels that are close to black (dark pixels)
dark_pixels = (image_rgba[:, :, 0] < threshold) & (image_rgba[:, :, 1] < threshold) & (image_rgba[:, :, 2] < threshold)

# Set alpha (transparency) channel to 0 for dark pixels (making them transparent)
image_rgba[dark_pixels, 3] = 0

# Create a new background (white background, can change to light gray by adjusting RGB values)
background_color = [255, 255, 255]  # White background
height, width = image.shape[:2]
new_image = np.full((height, width, 4), background_color + [255], dtype=np.uint8)  # White background with full alpha

# Copy the original image with transparency onto the new background
for y in range(height):
    for x in range(width):
        if image_rgba[y, x, 3] > 0:  # If the pixel is not fully transparent
            new_image[y, x] = image_rgba[y, x]

# Step 1: Create an edge mask to detect the borders of the brain
# Convert the image to grayscale
gray_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2GRAY)

#
_, brain_mask = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY)

# Use the Canny edge detector to find the edges of the brain
edges = cv2.Canny(gray_image, 100, 200)

# Debug edges
plt.imshow(edges, cmap='gray')
plt.axis('off')
plt.show()

# Step 2: Dilate the edges to create a larger region for blurring
kernel = np.ones((5, 5), np.uint8)  # Size of the dilation
dilated_edges = cv2.dilate(edges, kernel, iterations=1)

# Step 3: Create a blurred version of the image
blurred_image = cv2.GaussianBlur(new_image, (21, 21), 0)  # Apply blur to the entire image

# Step 4: Mask the blurred image to only affect the edges
# Create an inverse mask for the non-edge areas (keeping them sharp)
inverse_mask = cv2.bitwise_not(dilated_edges)

# Mask the original sharp image and blurred image
sharp_image = cv2.bitwise_and(new_image, new_image, mask=inverse_mask)
blurred_edge_image = cv2.bitwise_and(blurred_image, blurred_image, mask=dilated_edges)

# Combine the sharp and blurred images
final_image = cv2.add(sharp_image, blurred_edge_image)

# Display the image with the blurred edges
plt.imshow(cv2.cvtColor(final_image, cv2.COLOR_BGRA2RGBA))  # Convert BGRA to RGBA for display
plt.axis('off')  # Turn off the axis

# save in svg
plt.savefig("output_image.svg", format="svg", transparent=True)

# save the output image as PNG (without SVG limitations)
cv2.imwrite('output_image.png', final_image)