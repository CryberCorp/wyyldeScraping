import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import OUTPUT_JSON_FILE
from storage import load_profiles, save_profile
from extractors import extract_pseudo, extract_preferences, extract_description, extract_profile, extract_propos, extract_testimonials_final

def run_scraper(control):
    """Exécute le scraper en fonction du statut du contrôleur"""
    print("🕒 Connexion à Chrome...")
    options = webdriver.ChromeOptions()
    options.debugger_address = "127.0.0.1:9222"
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
        print("⚠️ Aucun profil Wyylde trouvé ! Ouvre un profil et relance.")
        driver.execute_script("alert('⚠️ Aucun profil Wyylde trouvé ! Ouvre un profil et relance le script.');")
        input("❌ Appuie sur ENTER pour quitter...")
        driver.quit()
        return

    driver.switch_to.window(wyylde_tab)

    all_profiles, existing_urls = load_profiles()

    last_status = None  

    while True:
        if not control.running:
            if last_status != "pause":
                print("⏸ En pause... Attente de démarrage.")
                last_status = "pause"
            time.sleep(1)
            continue  

        if last_status != "running":
            print("▶ Reprise du script...")
            last_status = "running"

        current_url = driver.current_url
        print(f"🌍 URL du profil actuel : {current_url}")

        if current_url in existing_urls:
            print(f"⚠️ L'URL {current_url} est déjà enregistrée. Ignoré !")
        else:
            profile_data = {
                "url": current_url,
                "pseudo": extract_pseudo(driver),
                **extract_preferences(driver),
                "description": extract_description(driver), 
                "profile": extract_profile(driver),
                "propos": extract_propos(driver),
                "testimonials": extract_testimonials_final(driver)
            }
            save_profile(profile_data)

        # 📌 Passer à la fiche suivante
        try:
            next_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "theme-pict-suiv-W"))
            )
            print("✅ Bouton 'Fiche suivante' trouvé !")
            driver.execute_script("arguments[0].click();", next_button)
            print("➡️ Passage au profil suivant...")

        except TimeoutException:
            print("🚨 Plus de bouton 'Fiche suivante' détecté. Tous les profils ont été traités.")
            driver.execute_script("alert('✅ Tous les profils ont été enregistrés !');")
            control.pause()
            while not control.running:
                if last_status != "pause":
                    print("⏸ Attente d'un redémarrage...")
                    last_status = "pause"
                time.sleep(2)

    print("\n✅ Tous les profils ont été enregistrés.")
    driver.quit()
