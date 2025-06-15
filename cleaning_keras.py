import zipfile
import json
import shutil
import os

def patch_keras_model_inplace(model_path="best_weights.keras"):
    temp_dir = "temp_keras_model"

    # Extract .keras zip contents
    with zipfile.ZipFile(model_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    model_json_path = os.path.join(temp_dir, "metadata.json")
    with open(model_json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Recursive function to fix RandomFlip layers
    def fix_random_flip(layer):
        if isinstance(layer, dict):
            if layer.get("class_name") == "RandomFlip":
                if "data_format" in layer.get("config", {}):
                    print(f"Setting 'data_format' to None in layer '{layer['config'].get('name')}'")
                    layer["config"]["data_format"] = None
            for v in layer.values():
                fix_random_flip(v)
        elif isinstance(layer, list):
            for item in layer:
                fix_random_flip(item)

    fix_random_flip(config)

    with open(model_json_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    # Repack the patched files into the same .keras file
    with zipfile.ZipFile(model_path, 'w') as zip_out:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, temp_dir)
                zip_out.write(full_path, arcname)

    shutil.rmtree(temp_dir)
    print(f"✅ Patched model saved in place: {model_path}")

# Run patch
patch_keras_model_inplace("best_weights.keras")
