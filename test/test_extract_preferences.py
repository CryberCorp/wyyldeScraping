import time
from selenium import webdriver
from selenium.webdriver.common.by import By

print("🚀 Test de récupération des préférences...")

# 🚀 Attacher Selenium à Chrome déjà ouvert
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"  # Se connecter à Chrome existant

try:
    print("🕒 Connexion à Chrome...")
    driver = webdriver.Chrome(options=options)
    print("✅ Selenium est connecté à Chrome !")

    # 📌 Trouver l'onglet Wyylde avec la bonne méthode
    wyylde_tab = None
    for tab in driver.window_handles:
        driver.switch_to.window(tab)
        current_url = driver.current_url
        print(f"🌍 Vérification onglet : {current_url}")

        if "app.wyylde.com/fr-fr/member" in current_url:
            wyylde_tab = tab
            print("✅ Onglet Wyylde trouvé !")
            break

    if not wyylde_tab:
        print("⚠️ ATTENTION : Aucun profil Wyylde trouvé !")
        driver.quit()
        exit()

    # 📌 Se placer sur l'onglet du profil
    driver.switch_to.window(wyylde_tab)
    time.sleep(2)  # Laisser le temps à la page de charger

    # 🔍 Récupération des éléments de "Je recherche"
    try:
        je_recherche_section = driver.find_element(By.XPATH, "//h4[contains(text(), 'Je recherche')]")
        je_recherche_elements = je_recherche_section.find_elements(By.XPATH, "./following-sibling::div//span")
        je_recherche = [el.text.strip() for el in je_recherche_elements if el.text.strip()]
        print(f"✅ Je recherche : {', '.join(je_recherche) if je_recherche else 'Aucune préférence trouvée'}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de 'Je recherche' ({e})")

    # 🔍 Récupération des éléments de "Mes envies"
    try:
        mes_envies_section = driver.find_element(By.XPATH, "//h4[contains(text(), 'Mes envies')]")
        mes_envies_elements = mes_envies_section.find_elements(By.XPATH, "./following-sibling::div//span")
        mes_envies = [el.text.strip() for el in mes_envies_elements if el.text.strip()]
        print(f"✅ Mes envies : {', '.join(mes_envies) if mes_envies else 'Aucune envie trouvée'}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de 'Mes envies' ({e})")

    driver.quit()

except Exception as e:
    print(f"❌ Erreur générale : {e}")
