import os
import json
import time
from sklearn.metrics import precision_score, f1_score
import matplotlib.pyplot as plt
import numpy as np

# Paths to JSON files
predicted_json_file = r"C:\3d model\car_features final.json"  # YOLO-generated file
ground_truth_json_file = r"C:\3d model\car features ground.json"  # Ground truth file

# **1. Load JSON files**
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    print(f"❌ Error: JSON file {file_path} not found!")
    return None

predicted_data = load_json(predicted_json_file)
ground_truth_data = load_json(ground_truth_json_file)

if predicted_data is None or ground_truth_data is None:
    exit()

# **2. Measure Detection Accuracy (Fixed)**
def calculate_detection_accuracy(predicted, ground_truth):
    predictions = []
    truths = []

    for frame, features in ground_truth.items():
        if frame in predicted:
            for key, value in features.items():
                if key in predicted[frame]:
                    # Convert values to strings to avoid issues with lists
                    predictions.append(str(predicted[frame][key]))
                    truths.append(str(value))
    
    return precision_score(truths, predictions, average='weighted', zero_division=0), f1_score(truths, predictions, average='weighted', zero_division=0)

# **3. Measure Processing Efficiency**
def measure_processing_time(function, *args):
    start_time = time.time()
    result = function(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

# **4. Measure Data Quality**
def check_data_quality(data):
    issues = {}
    for frame, features in data.items():
        for key in ["body_type", "car_bbox", "color", "grille_type", "fuel_type"]:
            if key not in features or features[key] in [None, "", [], {}]:
                if frame not in issues:
                    issues[frame] = []
                issues[frame].append(f"Missing or incorrect {key}")
    
    return issues

# **Run Efficiency Checks**
# Measure detection efficiency (Precision and F1-Score)
precision, f1 = calculate_detection_accuracy(predicted_data, ground_truth_data)
print(f"✅ Precision: {precision:.2f}")
print(f"✅ F1-Score: {f1:.2f}")

# Measure data processing time
_, processing_time = measure_processing_time(lambda: predicted_data)
print(f"✅ Processing Time: {processing_time:.4f} seconds")

# Measure data quality
data_issues = check_data_quality(predicted_data)
if data_issues:
    print("⚠️ Data Quality Issues Found:")
    print(json.dumps(data_issues, indent=4))
else:
    print("✅ Data Quality: No issues found!")

# **Plot Precision and F1-Score**
metrics = ['Precision', 'F1-Score']
values = [precision, f1]

# Create a bar plot for Precision and F1-Score
plt.figure(figsize=(6, 4))
plt.bar(metrics, values, color=['blue', 'green'])
plt.title('Precision and F1-Score')
plt.ylabel('Score')
plt.ylim(0, 1)

# Display the values on top of the bars
for i, v in enumerate(values):
    plt.text(i, v + 0.02, f'{v:.2f}', ha='center', color='black', fontweight='bold')

plt.show()
