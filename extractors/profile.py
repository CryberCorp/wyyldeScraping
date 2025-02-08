from selenium.webdriver.common.by import By
from .helpers import extract_section, determine_gender_labels

def extract_profile(driver):
    """Extrait toutes les informations d'un profil Wyylde"""
    profile_data = {"contexte": {}}

    # Extraction du Contexte
    profile_data["contexte"] = extract_section(driver, driver, "Contexte")

    # Déterminer le(s) label(s) à utiliser en fonction du sexe
    sexe_info = profile_data["contexte"].get("Sexe", "").lower()
    gender_keys = determine_gender_labels(sexe_info)
    is_couple = "couple" in sexe_info

    if is_couple:
        print("🔹 Profil couple détecté")
        try:
            profile_grid = driver.find_element(By.XPATH, "//div[contains(@class, 'grid-cols-2') or contains(@class, 'grid-cols-1')]")
            profile_blocks = profile_grid.find_elements(By.XPATH, "./div")
            if len(profile_blocks) >= 2:
                for i, gender in enumerate(gender_keys):
                    block = profile_blocks[i]
                    profile_data[gender] = {
                        "personnelles": extract_section(driver, block, "Informations personnelles"),
                        "physique": extract_section(driver, block, "Description physique"),
                    }
            else:
                print("⚠️ Impossible de trouver les deux sections distinctes, extraction partielle")
        except Exception as e:
            print(f"⚠️ Erreur lors de l'extraction du profil couple : {e}")
    else:
        print(f"🔹 Profil solo détecté ({gender_keys[0]})")
        profile_data[gender_keys[0]] = {
            "personnelles": extract_section(driver, driver, "Informations personnelles"),
            "physique": extract_section(driver, driver, "Description physique"),
        }

    return profile_data
