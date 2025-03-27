import os
import cv2
import numpy as np
import json

# Define paths
labels_dir = r"C:\3d model\runs\detect\predict\labels"  # YOLO labels path
images_dir = r"C:\3d model\frames"  # Frames path

# Check if labels directory exists
if not os.path.exists(labels_dir):
    print(f"Error: Labels directory '{labels_dir}' not found. Run YOLO detection first.")
    exit()

# Check if label files exist
label_files = os.listdir(labels_dir)
if not label_files:
    print("Error: No label files found! Make sure YOLO detection was successful.")
    exit()

print(f"Found {len(label_files)} label files. Processing...")

# Function to get the dominant color in a readable format
def get_dominant_color_name(image):
    pixels = image.reshape(-1, 3)
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    dominant_color = unique_colors[counts.argmax()]  # Most common color
    
    return rgb_to_color_name(dominant_color)

# Function to map RGB to color names
def rgb_to_color_name(rgb):
    color_ranges = {
        "Black": [(0, 0, 0), (50, 50, 50)],
        "White": [(200, 200, 200), (255, 255, 255)],
        "Gray": [(100, 100, 100), (200, 200, 200)],
        "Red": [(150, 0, 0), (255, 100, 100)],
        "Green": [(0, 150, 0), (100, 255, 100)],
        "Blue": [(0, 0, 150), (100, 100, 255)],
        "Yellow": [(150, 150, 0), (255, 255, 100)],
    }

    for color_name, (lower, upper) in color_ranges.items():
        if all(lower[i] <= rgb[i] <= upper[i] for i in range(3)):
            return color_name

    return "Unknown"

# Dictionary to store car data
car_data = []

# Process each label file
for label_file in label_files:
    if label_file.endswith(".txt"):
        image_file = os.path.join(images_dir, label_file.replace(".txt", ".jpg"))
        label_path = os.path.join(labels_dir, label_file)

        if not os.path.exists(image_file):
            print(f"Warning: Image file {image_file} not found, skipping.")
            continue

        print(f"Processing: {image_file}")

        # Read image
        image = cv2.imread(image_file)
        height, width, _ = image.shape

        # Read label file
        with open(label_path, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) < 5:
                    print(f"Skipping invalid label: {line}")
                    continue

                class_id, x_center, y_center, w, h = map(float, parts[:5])

                # Convert YOLO bbox to pixel values
                x1 = int((x_center - w / 2) * width)
                y1 = int((y_center - h / 2) * height)
                x2 = int((x_center + w / 2) * width)
                y2 = int((y_center + h / 2) * height)

                # Crop detected car region
                car_crop = image[y1:y2, x1:x2]

                # Check if the crop is valid
                if car_crop.size > 0:
                    dominant_color_name = get_dominant_color_name(car_crop)
                    car_data.append({
                        "image": os.path.basename(image_file),
                        
                        "color": dominant_color_name
                    })
                else:
                    print(f"Warning: Empty crop for {image_file}, skipping.")

# Save data to JSON
if car_data:
    with open("car_colors.json", "w") as json_file:
        json.dump(car_data, json_file, indent=4)
    print("✅ Car color data saved in car_colors.json")
else:
    print("❌ No valid cars detected!")
