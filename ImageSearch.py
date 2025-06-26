import requests
def get_bird_images(bird_name, per_page=4):
    taxa_url = "https://api.inaturalist.org/v1/taxa"
    taxa_params = {
        "q": bird_name,
        "rank": "species",
        "per_page": 1
    }
    taxa_response = requests.get(taxa_url, params=taxa_params)
    if taxa_response.status_code != 200:
        print(f"Failed to search taxa: {taxa_response.status_code}")
        return []

    taxa_data = taxa_response.json()
    if not taxa_data['results']:
        print(f"No taxa found for '{bird_name}'")
        return []

    taxon_id = taxa_data['results'][0]['id']

    # Step 2: Use taxon_id to get observations of that bird
    observations_url = "https://api.inaturalist.org/v1/observations"
    obs_params = {
        "taxon_id": taxon_id,
        "per_page": per_page
    }

    obs_response = requests.get(observations_url, params=obs_params)
    if obs_response.status_code != 200:
        print(f"Failed to get observations: {obs_response.status_code}")
        return []

    obs_data = obs_response.json()
    images = []

    for obs in obs_data['results']:
        photos = obs.get('photos', [])
        if photos:
            photo = photos[0]
            url = photo.get('url')
            if url:
                # Replace size keyword with 'original' for high-res image
                high_res_url = url.replace('square', 'original').replace('medium', 'original').split('?')[0]
                images.append(high_res_url)
    if not images:
        print("No images found.")
    return images

def get_verified_wikipedia_url(title):
    formatted_name = title.strip().title().replace(" ", "_")
    endpoint = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": formatted_name,
        "format": "json"
    }
    response = requests.get(endpoint, params=params)
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    if "-1" in pages:
        return None  # Page doesn't exist
    return f"https://en.wikipedia.org/wiki/{formatted_name}"