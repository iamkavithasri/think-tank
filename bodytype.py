import os
import json

# Paths
labels_dir = r"C:\3d model\runs\detect\predict\labels"  # YOLO label files
images_dir = r"C:\3d model\frames"  # Frames directory

# Define class IDs for car body types (Update based on your model)
BODY_TYPE_CLASSES = {
    0: "SUV",
    1: "Sedan",
    2: "Hatchback",
    3: "Coupe",
    4: "Convertible",
    5: "Pickup",
    6: "Van"
}

# Check if labels directory exists
if not os.path.exists(labels_dir):
    print(f"❌ Error: Labels directory '{labels_dir}' not found. Run YOLO detection first.")
    exit()

# Dictionary to store car body type data
car_data = []

# Process each label file
for label_file in os.listdir(labels_dir):
    if label_file.endswith(".txt"):
        image_file = os.path.join(images_dir, label_file.replace(".txt", ".jpg"))
        label_path = os.path.join(labels_dir, label_file)

        if not os.path.exists(image_file):
            print(f"⚠️ Warning: Image file {image_file} not found, skipping.")
            continue

        print(f"🔹 Processing: {image_file}")

        # Read label file
        with open(label_path, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) < 5:
                    print(f"⚠️ Skipping invalid label: {line}")
                    continue

                class_id = int(parts[0])  # First value is class ID

                # Check if class ID matches a body type
                if class_id in BODY_TYPE_CLASSES:
                    body_type = BODY_TYPE_CLASSES[class_id]
                    print(f"✅ Detected Car Type: {body_type}")

                    car_data.append({
                        "image": image_file,
                        "body_type": body_type
                    })

# Save data to JSON
if car_data:
    with open("car_body_types.json", "w") as json_file:
        json.dump(car_data, json_file, indent=4)
    print("✅ Car body type data saved in car_body_types.json")
else:
    print("❌ No car body types detected! Check YOLO class IDs.")
