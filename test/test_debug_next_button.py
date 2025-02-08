from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("🚀 Débogage du bouton 'Fiche suivante'...")

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

    # 📌 Attente du chargement complet
    print("🕒 Attente du chargement de la page...")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 📌 Récupérer **tous** les liens <a>
    all_links = driver.find_elements(By.TAG_NAME, "a")
    print(f"🔍 {len(all_links)} liens <a> trouvés sur la page.")

    found_button = []

    for link in all_links:
        try:
            link_text = link.text.strip()
            link_html = link.get_attribute("outerHTML")
            link_href = link.get_attribute("href")

            if "Fiche suivante" in link_text or "Fiche suivante" in link_html:
                found_button.append((link_text, link_html, link_href))
        except:
            pass  # Éviter l'erreur "stale element reference"

    if found_button:
        print("✅ Bouton 'Fiche suivante' trouvé dans les liens suivants :")
        for text, html, href in found_button:
            print(f"🔹 Texte : {text}\n🔹 HTML : {html}\n🔹 HREF : {href}\n")
    else:
        print("🚨 Aucun bouton 'Fiche suivante' détecté parmi les liens !")

    input("🔄 Appuie sur ENTER pour fermer...")

except Exception as e:
    print(f"❌ Erreur : {e}")
