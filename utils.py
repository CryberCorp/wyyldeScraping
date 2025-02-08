# utils.py
import time
from selenium.webdriver.common.by import By

def click_if_present(driver, xpath):
    """Clique sur un élément si présent."""
    try:
        bouton = driver.find_element(By.XPATH, xpath)
        bouton.click()
        time.sleep(2)  # Attendre le chargement
    except:
        pass  # Si le bouton n'existe pas, on continue

def get_text(driver, xpath):
    """Récupère du texte d'un élément, retourne None si absent."""
    try:
        return driver.find_element(By.XPATH, xpath).text.strip()
    except:
        return None
