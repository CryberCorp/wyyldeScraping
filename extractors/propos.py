from selenium.webdriver.common.by import By

def extract_propos(driver):
    """
    Extrait la section "A propos" du profil Wyylde et renvoie un dictionnaire contenant :
      - inscription : date d'inscription (ex: "12.02.2008")
      - connexion   : dernière connexion (ex: "08.02.2025")
      - visites     : nombre de visites (ex: "406218")
    
    La fonction se base sur la structure HTML suivante :
      - Un élément <h1> contenant "A propos"
      - Un conteneur parent avec la classe 'bg-brandWhite' qui englobe un élément <ol>
      - Chaque <li> de la liste contient deux <p> : le premier (label) et le second (valeur, en font-bold)
    
    Le mapping suivant est appliqué :
      - "Date d'inscription" → "inscription"
      - "Dernière connexion"  → "connexion"
      - "Nombre de visites"    → "visites"
    """
    propos_data = {}
    try:
        # Rechercher l'élément <h1> contenant "A propos"
        a_propos_header = driver.find_element(By.XPATH, "//h1[contains(text(),'A propos')]")
        # Remonter jusqu'au conteneur principal avec la classe 'bg-brandWhite'
        container = a_propos_header.find_element(By.XPATH, "./ancestor::div[contains(@class,'bg-brandWhite')]")
        # Récupérer l'élément <ol> contenant les <li>
        ol_element = container.find_element(By.TAG_NAME, "ol")
        li_elements = ol_element.find_elements(By.TAG_NAME, "li")
        
        # Mapping des labels normalisés vers nos clés souhaitées
        mapping = {
            "date d'inscription": "inscription",
            "dernière connexion": "connexion",
            "nombre de visites": "visites"
        }
        
        # Parcourir chaque <li> et extraire la valeur des balises <p>
        for li in li_elements:
            p_elements = li.find_elements(By.TAG_NAME, "p")
            if len(p_elements) >= 2:
                # Normalisation du texte du premier <p>
                raw_label = p_elements[0].text
                label = " ".join(raw_label.replace("\u00a0", " ").strip().lower().replace(":", "").split())
                if label in mapping:
                    key = mapping[label]
                    value = p_elements[1].text.strip()
                    propos_data[key] = value
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction de la section 'A propos': {e}")
    
    return propos_data
