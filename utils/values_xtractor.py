import os
import json
import re
from pathlib import Path

# Define the paths
base_path = Path("lib")
model_values_path = Path("model_values.json")
non_model_values_path = Path("non_modelvalues.json")

# Initialize dictionaries to store values
model_values = {}
non_model_values = {
    "event_names": [],
    "state_names": [],
    "function_names": [],
    "inputs_outputs": [],
    "imported_packages": [],
    "imported_classes": []
}

# Function to scan Dart files
def scan_dart_files():
    for file_path in base_path.rglob("*.dart"):
        with open(file_path, 'r') as file:
            content = file.read()
            parse_content(content, file_path.name)

# Function to parse Dart content
def parse_content(content, file_name):
    # Extract imported packages and classes
    imported_packages = re.findall(r"import '([^']+)';", content)
    imported_classes = re.findall(r'import package:([^"]+)";', content)
    non_model_values["imported_packages"].extend(imported_packages)
    non_model_values["imported_classes"].extend(imported_classes)
    
    # Extract class names
    class_name = re.findall(r'class (\w+)', content)
    
    if "model" in file_name.lower():
        # Extract model fields
        fields = re.findall(r'final (\w+) (\w+);', content)
        model_values[file_name] = {field[1]: field[0] for field in fields}
    else:
        # Extract event and state names
        event_names = re.findall(r'class (\w+Event)', content)
        state_names = re.findall(r'class (\w+State)', content)
        non_model_values["event_names"].extend(event_names)
        non_model_values["state_names"].extend(state_names)

        # Extract function names and their inputs/outputs
        functions = re.findall(r'\w+ (\w+)\((.*)\)', content)
        for function in functions:
            non_model_values["function_names"].append(function[0])
            non_model_values["inputs_outputs"].append({
                "function_name": function[0],
                "parameters": function[1]
            })

# Function to write JSON files
def write_json_files():
    with open(model_values_path, 'w') as model_file:
        json.dump(model_values, model_file, indent=4)
    
    with open(non_model_values_path, 'w') as non_model_file:
        json.dump(non_model_values, non_model_file, indent=4)
    
    print(f"Model values saved to {model_values_path}")
    print(f"Non-model values saved to {non_model_values_path}")

# Main function to execute the script
def main():
    scan_dart_files()
    write_json_files()

if __name__ == "__main__":
    main()
