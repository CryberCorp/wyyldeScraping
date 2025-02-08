import json
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By

def extract_text(element):
    """Retourne le texte d'un élément s'il existe, sinon NaN"""
    return element.text.strip() if element else "NaN"

def extract_section(driver, parent_element, section_name):
    """Scrape une section spécifique (Informations personnelles ou Description physique)"""
    section_data = {}
    try:
        section_block = parent_element.find_element(By.XPATH, f".//h4[contains(text(), '{section_name}')]/following-sibling::div")
        items = section_block.find_elements(By.XPATH, ".//div[@class='font-poppins text-blue-950 py-2']")
        
        for item in items:
            try:
                label = extract_text(item.find_element(By.XPATH, "./span[contains(@class, 'text-sm font-normal')]")).replace(" :", "")
                value = extract_text(item.find_element(By.XPATH, "./span[contains(@class, 'ml-1 text-sm font-bold')]"))
                section_data[label] = value
            except:
                continue
    except:
        print(f"⚠️ {section_name} non trouvé dans un bloc")
    
    return section_data

def determine_gender_labels(sexe_info):
    """Détermine les bons labels à utiliser pour les couples et solos"""
    sexe_info = sexe_info.lower()
    
    if "couple" in sexe_info:
        if "hétéro" in sexe_info:
            return "Homme Hétéro", "Femme Hétéro"
        elif "f bi" in sexe_info:
            return "Homme Hétéro", "Femme Bi"
        elif "h bi" in sexe_info:
            return "Homme Bi", "Femme Hétéro"
        elif "bi" in sexe_info:
            return "Homme Bi", "Femme Bi"
    else:
        if "homme" in sexe_info:
            if "bi" in sexe_info:
                return "Homme Bi",
            else:
                return "Homme Hétéro",
        elif "femme" in sexe_info:
            if "bi" in sexe_info:
                return "Femme Bi",
            else:
                return "Femme Hétéro",
        elif "travesti" in sexe_info:
            return "Travesti",
        elif "transgenre" in sexe_info:
            return "Transgenre",
        elif "gay" in sexe_info:
            return "Gay",
        elif "lesbienne" in sexe_info:
            return "Lesbienne",
    
    return "Autre",  # Cas non prévu

def extract_profile(driver):
    """Extrait toutes les informations d'un profil Wyylde"""
    profile_data = {"contexte": {}}

    # 📌 Extraire Contexte
    profile_data["contexte"] = extract_section(driver, driver, "Contexte")

    # 🔎 Vérifier le sexe
    sexe_info = profile_data["contexte"].get("Sexe", "").lower()
    gender_keys = determine_gender_labels(sexe_info)

    is_couple = "couple" in sexe_info

    # 📌 Extraction des données selon le type de profil
    if is_couple:
        print("🔹 Profil couple détecté")

        # Trouver le bloc contenant les deux profils
        profile_grid = driver.find_element(By.XPATH, "//div[contains(@class, 'grid-cols-2') or contains(@class, 'grid-cols-1')]")

        # Récupérer les deux sous-blocs correspondant à l'homme et à la femme
        profile_blocks = profile_grid.find_elements(By.XPATH, "./div")

        if len(profile_blocks) >= 2:
            for i, gender in enumerate(gender_keys):
                block = profile_blocks[i]  # Prend l'élément correspondant
                profile_data[gender] = {
                    "personnelles": extract_section(driver, block, "Informations personnelles"),
                    "physique": extract_section(driver, block, "Description physique"),
                }
        else:
            print("⚠️ Impossible de trouver les deux sections distinctes, extraction partielle")

    else:
        print(f"🔹 Profil solo détecté ({gender_keys[0]})")
        profile_data[gender_keys[0]] = {
            "personnelles": extract_section(driver, driver, "Informations personnelles"),
            "physique": extract_section(driver, driver, "Description physique"),
        }

    return profile_data


# 🚀 Connexion Selenium
print("🚀 Test de récupération des informations du profil...")
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"  # Connexion à Chrome existant

try:
    print("🕒 Connexion à Chrome...")
    driver = webdriver.Chrome(options=options)
    print("✅ Selenium est connecté à Chrome !")

    # 📌 Trouver l'onglet Wyylde avec un profil
    wyylde_tab = None
    for tab in driver.window_handles:
        driver.switch_to.window(tab)
        current_url = driver.current_url
        print(f"🌍 Vérification onglet : {current_url}")

        if "app.wyylde.com" in current_url:  # Vérifier qu'on est bien sur un profil
            wyylde_tab = tab
            print("✅ Onglet Wyylde trouvé !")
            break

    if not wyylde_tab:
        print("⚠️ ATTENTION : Aucun profil Wyylde trouvé !")
        driver.quit()
        exit()

    driver.switch_to.window(wyylde_tab)

    # 🔍 Extraction du profil
    profile_data = extract_profile(driver)

    # 📌 Sauvegarde en JSON
    with open("profile_data.json", "w", encoding="utf-8") as f:
        json.dump(profile_data, f, ensure_ascii=False, indent=4)

    print("\n✅ Profil extrait et sauvegardé avec succès : `profile_data.json`")
    print(json.dumps(profile_data, ensure_ascii=False, indent=4))

    driver.quit()

except Exception as e:
    print(f"❌ Erreur générale : {e}")
    traceback.print_exc()
