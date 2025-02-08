# extractors/testimonials.py
import time
from selenium.webdriver.common.by import By
from emoji_handler import replace_wyylde_emojis  # si nécessaire pour adapter les emojis dans les messages

def get_testimonial_tab_data(driver):
    data = {}
    try:
        tabs = driver.find_elements(By.XPATH, "//nav[contains(@class,'onglet2')]//li[a/b[contains(.,'Témoignages')]]")
        if not tabs:
            data["testimonial_present"] = False
            return data
        data["testimonial_present"] = True
        tab = tabs[0]
        num_elem = tab.find_element(By.XPATH, ".//strong[contains(@class,'number')]")
        data["testimonial_count"] = num_elem.text.strip()
        tab.find_element(By.TAG_NAME, "a").click()
        time.sleep(0.0)
    except Exception as e:
        print("Erreur dans get_testimonial_tab_data :", e)
    return data

def count_testimonials(driver):
    try:
        articles = driver.find_elements(By.XPATH,
            "//article[contains(@class, 'borderBox') and contains(@class, 'boxShadow') and contains(@class, 'MB15')]")
        return len(articles)
    except Exception as e:
        print("Erreur lors du comptage des témoignages :", e)
        return 0

def wait_for_testimonials(driver, expected_count, timeout=120):
    start = time.time()
    while True:
        count = count_testimonials(driver)
        print("Nombre actuel de témoignages dans le DOM :", count)
        if count == expected_count:
            print("Tous les témoignages sont chargés.")
            return
        if time.time() - start > timeout:
            print("Timeout atteint après 120 secondes.")
            return
        driver.execute_script("window.scrollBy(0, window.innerHeight * 10);")
        time.sleep(0.01)

def extract_testimonials(driver):
    testimonials = []
    try:
        articles = driver.find_elements(By.XPATH,
            "//article[contains(@class, 'borderBox') and contains(@class, 'boxShadow') and contains(@class, 'MB15')]")
        for article in articles:
            testimonial = {}
            try:
                a_elem = article.find_element(By.CSS_SELECTOR, "a.colorTheme.vaM")
                href = a_elem.get_attribute("href")
                testimonial["member_id"] = href.split("/")[-1]
            except Exception as e:
                print("Erreur extraction member_id :", e)
            try:
                time_elem = article.find_element(By.TAG_NAME, "time")
                testimonial["datetime"] = time_elem.get_attribute("datetime")
            except Exception as e:
                print("Erreur extraction datetime :", e)
            try:
                p_elem = article.find_element(By.CSS_SELECTOR, "p.FS14.oWrap")
                message = p_elem.text.strip()
                # Optionnel : adapter les emojis dans le message
                testimonial["message"] = replace_wyylde_emojis(message)
            except Exception as e:
                print("Erreur extraction message :", e)
            testimonials.append(testimonial)
    except Exception as e:
        print("Erreur extraction des témoignages :", e)
    return testimonials

def filter_duplicates(testimonials):
    seen = set()
    filtered = []
    for t in testimonials:
        key = (t.get("member_id"), t.get("datetime"))
        if key not in seen:
            filtered.append(t)
            seen.add(key)
    return filtered

def extract_testimonials_final(driver):
    """
    Processus global pour récupérer les témoignages :
      1. Récupérer les infos de l’onglet témoignages.
      2. Si présent, attendre (via scrolling) que le DOM contienne exactement le nombre attendu,
         ou jusqu’au timeout de 120 sec.
      3. Extraire ensuite tous les témoignages.
      4. Filtrer les doublons.
      5. Retourner le résultat final (dictionnaire avec les infos de l’onglet et la liste des témoignages).
    """
    data = get_testimonial_tab_data(driver)
    if not data.get("testimonial_present"):
        data["testimonials"] = []
        return data
    try:
        expected = int(data.get("testimonial_count", "0"))
    except ValueError:
        expected = 0
    wait_for_testimonials(driver, expected, timeout=120)
    testimonials = extract_testimonials(driver)
    unique_testimonials = filter_duplicates(testimonials)
    if len(unique_testimonials) < len(testimonials):
        print("Avertissement : des doublons ont été détectés et filtrés.")
    data["testimonials"] = unique_testimonials
    return data
