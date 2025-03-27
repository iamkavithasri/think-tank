import cv2
import numpy as np
import os

# Path to YOLO labels and images
labels_dir = r"C:\3d model\runs\detect\predict\labels"
images_dir = r"C:\3d model\frames"

# Define a function to get the dominant color as a name
def get_dominant_color_name(image):
    # Convert image to list of pixels
    pixels = image.reshape(-1, 3)
    # Find the most frequent color
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    dominant_color = unique_colors[counts.argmax()]  # Get the most common color
    
    # Map RGB values to a color name (basic approximation)
    dominant_color_name = rgb_to_color_name(dominant_color)
    
    return dominant_color_name

# Map RGB values to basic color names
def rgb_to_color_name(rgb):
    # Define color ranges (simplified)
    color_ranges = {
        "Red": [(150, 0, 0), (255, 100, 100)],
        "Green": [(0, 150, 0), (100, 255, 100)],
        "Blue": [(0, 0, 150), (100, 100, 255)],
        "Yellow": [(150, 150, 0), (255, 255, 100)],
        "Black": [(0, 0, 0), (50, 50, 50)],
        "White": [(200, 200, 200), (255, 255, 255)],
        "Gray": [(100, 100, 100), (200, 200, 200)],
    }

    # Check which color range the dominant color belongs to
    for color, (lower, upper) in color_ranges.items():
        if all(lower[i] <= rgb[i] <= upper[i] for i in range(3)):
            return color
    
    return "Unknown"  # If no match found, return Unknown

# Process each labeled image
for label_file in os.listdir(labels_dir):
    if label_file.endswith(".txt"):
        image_file = os.path.join(images_dir, label_file.replace(".txt", ".jpg"))
        label_path = os.path.join(labels_dir, label_file)

        if os.path.exists(image_file):
            image = cv2.imread(image_file)
            height, width, _ = image.shape

            # Read YOLO label file
            with open(label_path, "r") as file:
                for line in file:
                    parts = line.strip().split()
                    class_id, x_center, y_center, w, h = map(float, parts[:5])

                    # Convert YOLO coordinates to pixel values
                    x1 = int((x_center - w / 2) * width)
                    y1 = int((y_center - h / 2) * height)
                    x2 = int((x_center + w / 2) * width)
                    y2 = int((y_center + h / 2) * height)

                    # Crop the detected car
                    car_crop = image[y1:y2, x1:x2]

                    # Get dominant color name
                    dominant_color_name = get_dominant_color_name(car_crop)
                    print(f"Car detected in {image_file} - Dominant Color: {dominant_color_name}")
