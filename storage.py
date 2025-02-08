import json
from config import OUTPUT_JSON_FILE

def load_profiles():
    """Charge les profils existants depuis data.json"""
    try:
        with open(OUTPUT_JSON_FILE, "r", encoding="utf-8") as f:
            all_profiles = json.load(f)
            existing_urls = {profile["url"] for profile in all_profiles}
        return all_profiles, existing_urls
    except (FileNotFoundError, json.JSONDecodeError):
        return [], set()

def save_profile(profile_data):
    """Ajoute un profil à data.json"""
    all_profiles, _ = load_profiles()
    all_profiles.append(profile_data)
    
    with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(all_profiles, f, ensure_ascii=False, indent=4)

    print(f"✅ Profil enregistré dans '{OUTPUT_JSON_FILE}'.")
