from ImageSearch import get_bird_images
import json
import pandas as pd
import wikipedia

def assign_category(name: str) -> str:
    name = name.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in name for keyword in keywords):
            return category
    return "unknown"

def assign_habitat(category: str) -> str:
    return DEFAULT_HABITATS.get(category, "Various habitats")

CATEGORY_KEYWORDS = {
    "raptor": ["hawk", "eagle", "falcon", "owl", "vulture", "harrier", "kite"],
    "waterbird": ["duck", "goose", "heron", "egret", "pelican", "tern", "gull", "loon", "grebe", "coot"],
    "songbird": ["warbler", "sparrow", "finch", "thrush", "oriole", "robin", "wren", "swallow", "bunting", "starling"],
    "common": ["pigeon", "dove", "crow", "jay", "blackbird", "magpie", "cardinal"],
    "woodpecker": ["woodpecker", "sapsucker", "flicker"],
    "shorebird": ["sandpiper", "plover", "avocet", "stilt"],
    "gamebird": ["quail", "pheasant", "grouse", "turkey"]
}

# Default habitats based on categories
DEFAULT_HABITATS = {
    "raptor": "Open woodlands, cliffs, or urban high-rises",
    "waterbird": "Wetlands, lakes, rivers, and coastal shores",
    "songbird": "Forests, gardens, and shrublands",
    "common": "Urban areas, parks, and farms",
    "woodpecker": "Forests and wooded areas",
    "shorebird": "Sandy shores, mudflats, wetlands",
    "gamebird": "Grasslands, fields, and forests",
    "unknown": "Various habitats"
}

with open('bird_classes.json', 'r') as f:
    class_data = json.load(f)

class_data= pd.DataFrame(class_data)
scientific_names=list(class_data["name"])[:100]
labels=list(class_data["common_name"])[:100]

bird_images=[]

for index,label in enumerate(labels):
    print("Processing:" ,label,"bird. Number:",index+1)
    scientific= scientific_names[index]
    image= get_bird_images(label, per_page=1)
    category = assign_category(label)
    habitat = assign_habitat(category)

    try:
        summary = wikipedia.summary(labels, sentences=1)
    except:
        summary = "No description available."

    if image==[]:
        bird_images.append({"name": label,
                            "scientificName": scientific,
                            "category": category,
                            "habitat": habitat,
                            "description": summary,
                            "image": "https://via.placeholder.com/600x400?text=No+Image+Found"})
    else:
        bird_images.append({"name": label,
                            "scientificName": scientific,
                            "category": category,
                            "habitat": habitat,
                            "description": summary,
                            "image": image[0]})

with open("static/data/bird_image_database.json", "w", encoding="utf-8") as f:
        json.dump(bird_images, f, ensure_ascii=False, indent=2)
print(f"Saved {len(bird_images)} entries to bird_image_database.json")