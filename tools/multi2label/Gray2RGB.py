import numpy as np
import cv2
import os


def color_mapping(gray_value):
    if gray_value == 50:
        return (115, 178, 115)  # Blue
    elif gray_value == 100:
        return (242, 219, 151)  # Green
    elif gray_value == 150:
        return (115, 255, 255)  # Red
    elif gray_value == 200:
        return (190, 190, 255)  # Yellow
    elif gray_value == 250:
        return (190, 234, 250)  # Cyan
    else:
        return (0, 0, 0)  # Black


input_folder = '../output/output4.4/label'
output_folder = '../output/output4.4/labelRGB'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process images in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Load the grayscale image
        gray_image = cv2.imread(os.path.join(input_folder, filename), cv2.IMREAD_GRAYSCALE)

        # Create an empty color image
        color_image = np.zeros((gray_image.shape[0], gray_image.shape[1], 3), dtype=np.uint8)

        # Apply color mapping
        for i in range(gray_image.shape[0]):
            for j in range(gray_image.shape[1]):
                gray_value = gray_image[i, j]
                color = color_mapping(gray_value)
                color_image[i, j] = color

        # Save the color mapped image
        output_filename = os.path.splitext(filename)[0] + '_color_mapped.png'
        output_path = os.path.join(output_folder, output_filename)
        cv2.imwrite(output_path, color_image)
