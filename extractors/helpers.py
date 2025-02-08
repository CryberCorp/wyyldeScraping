from selenium.webdriver.common.by import By

def extract_text(element):
    """Retourne le texte d'un élément s'il existe, sinon 'NaN'."""
    return element.text.strip() if element else "NaN"

def extract_section(driver, parent_element, section_name):
    """Scrape une section spécifique (ex. Informations personnelles, Description physique)"""
    section_data = {}
    try:
        section_block = parent_element.find_element(By.XPATH, f".//h4[contains(text(), '{section_name}')]/following-sibling::div")
        items = section_block.find_elements(By.XPATH, ".//div[@class='font-poppins text-blue-950 py-2']")
        for item in items:
            try:
                label = extract_text(item.find_element(By.XPATH, "./span[contains(@class, 'text-sm font-normal')]")).replace(" :", "")
                value = extract_text(item.find_element(By.XPATH, "./span[contains(@class, 'ml-1 text-sm font-bold')]"))
                section_data[label] = value
            except Exception:
                continue
    except Exception:
        print(f"⚠️ {section_name} non trouvé dans un bloc")
    return section_data

def determine_gender_labels(sexe_info):
    """Détermine les bons labels à utiliser en fonction des infos sur le sexe"""
    sexe_info = sexe_info.lower()
    if "couple" in sexe_info:
        if "hétéro" in sexe_info:
            return ("Homme Hétéro", "Femme Hétéro")
        elif "f bi" in sexe_info:
            return ("Homme Hétéro", "Femme Bi")
        elif "h bi" in sexe_info:
            return ("Homme Bi", "Femme Hétéro")
        elif "bi" in sexe_info:
            return ("Homme Bi", "Femme Bi")
    else:
        if "homme" in sexe_info:
            return ("Homme Bi",) if "bi" in sexe_info else ("Homme Hétéro",)
        elif "femme" in sexe_info:
            return ("Femme Bi",) if "bi" in sexe_info else ("Femme Hétéro",)
        elif "travesti" in sexe_info:
            return ("Travesti",)
        elif "transgenre" in sexe_info:
            return ("Transgenre",)
        elif "gay" in sexe_info:
            return ("Gay",)
        elif "lesbienne" in sexe_info:
            return ("Lesbienne",)
    return ("Autre",)
