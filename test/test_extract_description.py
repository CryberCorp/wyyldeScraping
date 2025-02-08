import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re  # Module regex pour extraire l'emoji

print("🚀 Test de récupération de la description avec emojis et images...")

# 🚀 Attacher Selenium à Chrome déjà ouvert
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"

try:
    print("🕒 Connexion à Chrome...")
    driver = webdriver.Chrome(options=options)
    print("✅ Selenium est connecté à Chrome !")

    # 📌 Trouver l'onglet Wyylde contenant un profil
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

    # 📌 Récupérer la description avec les emojis insérés au bon endroit
    try:
        description_element = driver.find_element(By.CSS_SELECTOR, "div[style*='white-space: pre-line']")
        description_html = description_element.get_attribute("innerHTML")  # Récupérer le HTML brut

        # 📌 Remplacement des emojis/images par du texte lisible
        emoji_images = description_element.find_elements(By.CSS_SELECTOR, "img.emojione")

        for img in emoji_images:
            img_src = img.get_attribute("src")  # Extrait l'URL de l'image
            match = re.search(r"/smilies/([^.]+)", img_src)  # Regex pour extraire le nom entre `/smilies/` et `.`

            if match:
                emoji_name = match.group(1)  # Récupère le nom du fichier (ex: "coeur", "interdit", "BOUNCE")
                emoji_tag = f"smilWyylde#{emoji_name}"  # Format standardisé

                # Remplace chaque balise <img> par son équivalent textuel
                description_html = description_html.replace(img.get_attribute("outerHTML"), f" {emoji_tag} ")

        # Nettoyage du texte final
        description = description_html.replace("\n\n", "\n").replace("&nbsp;", " ").strip()

        print(f"✅ Description récupérée :\n{description}")

    except Exception as e:
        print(f"❌ Erreur : Impossible de récupérer la description ({e})")

    driver.quit()

except Exception as e:
    print(f"❌ Erreur générale : {e}")
