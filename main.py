import threading
from scraper import run_scraper
from control import ScriptControl

if __name__ == "__main__":
    control = ScriptControl()

    # Démarrer le scraper dans un thread
    scraper_thread = threading.Thread(target=run_scraper, args=(control,))
    scraper_thread.daemon = True  
    scraper_thread.start()

    # Lancer l'interface graphique
    control.launch()
