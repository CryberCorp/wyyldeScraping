import json
import traceback
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def extract_propos(driver):
    """
    Extrait la section "A propos" et renvoie un dictionnaire contenant :
      - inscription (issu de "Date d'inscription")
      - connexion (issu de "Dernière connexion")
      - visites (issu de "Nombre de visites")
    On récupère uniquement le texte présent dans les balises <p class="font-bold">.
    """
    propos_data = {}
    try:
        # Rechercher l'élément <h1> contenant "A propos"
        a_propos_header = driver.find_element(By.XPATH, "//h1[contains(text(),'A propos')]")
        print("✅ Header 'A propos' trouvé")
        
        # Remonter jusqu'au conteneur principal contenant la classe 'bg-brandWhite'
        container = a_propos_header.find_element(By.XPATH, "./ancestor::div[contains(@class,'bg-brandWhite')]")
        print("✅ Container 'bg-brandWhite' trouvé")
        
        # Récupérer l'élément <ol> qui contient les <li>
        ol_element = container.find_element(By.TAG_NAME, "ol")
        li_elements = ol_element.find_elements(By.TAG_NAME, "li")
        print(f"✅ {len(li_elements)} élément(s) <li> trouvé(s)")
        
        # Mapping des labels (en minuscule) vers nos clés désirées
        mapping = {
            "date d'inscription": "inscription",
            "dernière connexion": "connexion",
            "nombre de visites": "visites"
        }
        
        # Pour chaque li, récupérer le label (premier <p>) et la valeur (deuxième <p>)
        for li in li_elements:
            p_elements = li.find_elements(By.TAG_NAME, "p")
            if len(p_elements) >= 2:
                raw_label = p_elements[0].text
                # Normalisation du label : suppression des espaces non standards et des deux-points, et mise en minuscule
                label = " ".join(raw_label.replace("\u00a0", " ").strip().lower().replace(":", "").split())
                print("   -> Label trouvé :", repr(label))
                if label in mapping:
                    key = mapping[label]
                    value = p_elements[1].text.strip()
                    propos_data[key] = value
                    print(f"      => Extraction : {key} = {value}")
                else:
                    print("      => Label ignoré :", repr(label))
            else:
                print("   -> Moins de 2 balises <p> dans ce li, ignoré.")
    except Exception as e:
        print("❌ Erreur lors de l'extraction de la section 'A propos':", e)
        traceback.print_exc()
    return propos_data

def main():
    print("🚀 Test de récupération de la section 'A propos'...")
    options = webdriver.ChromeOptions()
    options.debugger_address = "127.0.0.1:9222"  # Connexion à Chrome déjà lancé en mode debug

    try:
        print("🕒 Connexion à Chrome...")
        driver = webdriver.Chrome(options=options)
        print("✅ Selenium est connecté à Chrome !")
        
        # Parcourir tous les onglets et sélectionner celui contenant le profil Wyylde
        wyylde_tab = None
        for tab in driver.window_handles:
            driver.switch_to.window(tab)
            current_url = driver.current_url
            print("🌍 Onglet en cours :", current_url)
            if "app.wyylde.com/fr-fr/member" in current_url:
                wyylde_tab = tab
                print("✅ Onglet Wyylde trouvé !")
                break
        
        if not wyylde_tab:
            print("⚠️ Aucun onglet Wyylde trouvé !")
            driver.quit()
            return

        # Se placer sur l'onglet Wyylde et attendre que la page soit chargée
        driver.switch_to.window(wyylde_tab)
        time.sleep(2)
        
        # Extraction de la section "A propos"
        propos_data = extract_propos(driver)
        
        # Sauvegarde des données extraites dans un fichier JSON
        with open("propos_data.json", "w", encoding="utf-8") as f:
            json.dump(propos_data, f, ensure_ascii=False, indent=4)
        
        print("\n✅ Données extraites pour 'A propos' :")
        print(json.dumps(propos_data, ensure_ascii=False, indent=4))
        
        driver.quit()
    except Exception as e:
        print("❌ Erreur générale :", e)
        traceback.print_exc()

if __name__ == "__main__":
    main()
