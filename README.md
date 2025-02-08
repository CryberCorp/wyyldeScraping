# wyyldeScraping
[Python] Web scraping for Wyylde

à corriger : dans cas de traitement de plusieurs milliers de profils > probleme ram surchager (saturer la mémoire) en local > car lit + réécrit l'intégralité du data.json > donc probleme de saturation

Solution possible : Stockage incrémental ou en streaming ex : sqlite

 la méthode de stockage actuelle > relis intégralité de data.json (donc poids sur ram) + reecriture. 

 Le problème potentiel vient de la méthode de stockage :

La fonction load_profiles() dans storage.py lit l'intégralité du fichier JSON (OUTPUT_JSON_FILE) pour charger tous les profils déjà sauvegardés.
À chaque nouveau profil, save_profile(profile_data) appelle load_profiles(), ajoute le nouveau profil à la liste existante, puis réécrit l'ensemble du fichier.
Si je traites des milliers de profils, la taille de ce fichier et donc la liste en mémoire augmentera, ce qui peut saturer la mémoire. Cette accumulation est bien une référence globale qui se reconstruit à chaque écriture.