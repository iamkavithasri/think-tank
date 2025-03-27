import json
import os

# List of JSON files to merge
json_files = [
    "car_body_types.json",
    "car_colors.json",
    "car_wheels.json",
    "car_grilles.json",
    "car_fuel_types.json"
]

# Dictionary to store combined data
combined_data = {}

# Read each JSON file and merge data
for json_file in json_files:
    if os.path.exists(json_file):
        print(f"✅ Reading {json_file}...")
        with open(json_file, "r") as file:
            data = json.load(file)

            for item in data:
                image_path = item["image"]

                # Initialize entry if missing
                if image_path not in combined_data:
                    combined_data[image_path] = {
                        "image": image_path,
                        "features": {
                            "wheel_size": [784, 460],  # ✅ Default wheel size
                            "color": "Black",          # ✅ Default color
                            "body_type": "Unknown",
                            "grille_type": "Unknown",
                            "fuel_type": "Unknown"
                        }
                    }

                # Merge attributes into "features"
                for key, value in item.items():
                    if key != "image":
                        combined_data[image_path]["features"][key] = value

# Save merged data
with open("car_features.json", "w") as output_file:
    json.dump(list(combined_data.values()), output_file, indent=4)

print("✅ Merging complete! Check car_features.json")
