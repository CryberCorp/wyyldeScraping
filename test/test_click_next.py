from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("🚀 Défilement automatique des profils...")

# 🚀 Connexion à Chrome
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"

try:
    print("🕒 Connexion à Chrome...")
    driver = webdriver.Chrome(options=options)
    print("✅ Selenium est connecté à Chrome !")

    # 📌 Sélectionner l'onglet Wyylde
    wyylde_tab = None
    all_tabs = driver.window_handles

    for tab in all_tabs:
        driver.switch_to.window(tab)
        current_url = driver.current_url
        print(f"🌍 Vérification onglet : {current_url}")

        if "wyylde.com/fr-fr/member" in current_url:
            print("✅ Onglet Wyylde trouvé !")
            wyylde_tab = tab
            break

    if not wyylde_tab:
        print("🚨 ERREUR : Aucun onglet Wyylde détecté !")
        input("🔄 Appuie sur ENTER pour fermer...")
        driver.quit()
        exit()

    # 📌 Défilement en boucle avec pause
    while True:
        print("🕒 Pause de 3 secondes sur le profil actuel...")
        time.sleep(3)  # Pause sur chaque profil avant de passer au suivant

        # 📌 Récupérer le bouton "Fiche suivante"
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "theme-pict-suiv-W"))
            )

            print("✅ Bouton 'Fiche suivante' trouvé !")
            print("🔄 Clic via JavaScript...")

            # 📌 Clic en JavaScript sur le vrai bouton <b>
            driver.execute_script("arguments[0].click();", next_button)

            time.sleep(3)  # Attente pour le chargement du nouveau profil
            print("✅ Changement de profil effectué avec succès !")

        except Exception as e:
            print(f"❌ Erreur : Impossible de cliquer sur 'Fiche suivante' ({e})")
            break  # Arrêter la boucle si une erreur survient

except Exception as e:
    print(f"❌ Erreur critique : {e}")

print("🔄 Appuie sur ENTER pour arrêter...")
input()
driver.quit()
