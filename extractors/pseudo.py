from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def extract_pseudo(driver):
    """Récupère le pseudo de l'utilisateur"""
    try:
        pseudo_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3.titleTheme"))
        )
        return pseudo_element.get_attribute("title").strip()
    except TimeoutException:
        print("❌ Impossible de récupérer le pseudo après 30 secondes.")
        return "NaN"
