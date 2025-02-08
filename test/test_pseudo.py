import time
from selenium import webdriver
from selenium.webdriver.common.by import By

print("🚀 Test de récupération du pseudo...")

# 🚀 Attacher Selenium à Chrome déjà ouvert
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"  # Se connecter à Chrome existant

try:
    print("🕒 Connexion à Chrome...")
    driver = webdriver.Chrome(options=options)
    print("✅ Selenium est connecté à Chrome !")

    # 📌 Trouver l'onglet Wyylde
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

    # 📌 Récupérer le pseudo (Méthode 1 : via le <div class="truncate">)
    try:
        pseudo_element = driver.find_element(By.CSS_SELECTOR, "h3.titleTheme div.truncate")
        pseudo = pseudo_element.text.strip()
        print(f"✅ Pseudo trouvé (Méthode 1) : {pseudo}")
    except Exception as e:
        print(f"❌ Erreur (Méthode 1) : Impossible de récupérer le pseudo ({e})")

    # 📌 Récupérer le pseudo (Méthode 2 : via l'attribut title du <h3>)
    try:
        pseudo_element_alt = driver.find_element(By.CSS_SELECTOR, "h3.titleTheme")
        pseudo_alt = pseudo_element_alt.get_attribute("title").strip()
        print(f"✅ Pseudo trouvé (Méthode 2) : {pseudo_alt}")
    except Exception as e:
        print(f"❌ Erreur (Méthode 2) : Impossible de récupérer le pseudo ({e})")

    driver.quit()

except Exception as e:
    print(f"❌ Erreur générale : {e}")
