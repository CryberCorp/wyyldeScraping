from selenium.webdriver.common.by import By

def extract_preferences(driver):
    """Récupère les préférences du profil (recherche et envies)"""
    preferences = {
        "recherche": "NaN",
        "envies": "NaN"
    }
    try:
        recherche_section = driver.find_element(By.XPATH, "//h4[contains(text(), 'Je recherche')]")
        recherche_elements = recherche_section.find_elements(By.XPATH, "./following-sibling::div//span")
        recherche_values = [el.text.strip() for el in recherche_elements if el.text.strip()]
        preferences["recherche"] = recherche_values if recherche_values else "NaN"
    except Exception:
        print("❌ Impossible de récupérer 'Je recherche'.")
    try:
        envies_section = driver.find_element(By.XPATH, "//h4[contains(text(), 'Mes envies')]")
        envies_elements = envies_section.find_elements(By.XPATH, "./following-sibling::div//span")
        envies_values = [el.text.strip() for el in envies_elements if el.text.strip()]
        preferences["envies"] = envies_values if envies_values else "NaN"
    except Exception:
        print("❌ Impossible de récupérer 'Mes envies'.")
    return preferences
