from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
import time

# 🚀 Configuration pour attacher Selenium à Chrome déjà ouvert
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"  # Se connecte au Chrome existant

try:
    print("🚀 Tentative de connexion à Chrome...")
    driver = webdriver.Chrome(options=options)
    print("✅ Selenium est bien connecté à Chrome !")

    # 📌 Vérifier que Selenium contrôle bien Chrome
    driver.execute_script("alert('✅ Selenium contrôle cette fenêtre Chrome !');")
    print("✅ Alerte envoyée dans Chrome.")

    # 📌 Attendre 3 secondes pour voir l’alerte avant de la fermer
    time.sleep(10)

    # 📌 Fermer automatiquement l'alerte
    try:
        alert = driver.switch_to.alert
        print(f"🔔 Alerte détectée : {alert.text}")
        alert.accept()
        print("✅ Alerte fermée avec succès.")
    except NoAlertPresentException:
        print("✅ Aucune alerte détectée.")

    # 📌 Charger une page de test
    driver.get("https://www.google.com")
    print("✅ Google est chargé avec succès.")

    input("Appuie sur ENTER pour quitter...")
    driver.quit()

except Exception as e:
    print(f"❌ Erreur : {e}")
