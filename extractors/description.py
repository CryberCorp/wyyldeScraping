from selenium.webdriver.common.by import By
from emoji_handler import replace_wyylde_emojis

def extract_description(driver):
    """Récupère la description complète et applique la transformation des emojis"""
    try:
        description_element = driver.find_element(By.CSS_SELECTOR, "div[style*='white-space: pre-line']")
        description_html = description_element.get_attribute("innerHTML")
        description_cleaned = replace_wyylde_emojis(description_html)
        description = description_cleaned.replace("\n\n", "\n").replace("&nbsp;", " ").strip()
        return description if description else "NaN"
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction de la description ({e})")
        return "NaN"
