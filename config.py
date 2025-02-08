import os

# 🔧 Configuration générale
DEBUG = True  # Active/Désactive les logs détaillés

# 🔗 URLs
WYYLDE_URL = "https://app.wyylde.com/"

# 📂 Chemins des fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_DRIVER_PATH = os.path.join(BASE_DIR, "chromedriver.exe")  # Chemin dynamique
OUTPUT_JSON_FILE = os.path.join(BASE_DIR, "data.json")  # Toujours dans le dossier du script

# 🖥️ Connexion à Chrome déjà ouvert (mode débogage)
CHROME_DEBUGGER_ADDRESS = "127.0.0.1:9222"
