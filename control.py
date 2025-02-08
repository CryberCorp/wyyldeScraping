import tkinter as tk
import time

class ScriptControl:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Contrôle du Script")
        self.root.geometry("300x150")

        self.running = False  # Par défaut, en pause

        self.status_label = tk.Label(self.root, text="🔴 En pause", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.start_button = tk.Button(self.root, text="▶ Démarrer", command=self.start)
        self.start_button.pack(pady=5)

        self.pause_button = tk.Button(self.root, text="⏸ Pause", command=self.pause)
        self.pause_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="⏹ Arrêter", command=self.stop)
        self.stop_button.pack(pady=5)

    def start(self):
        self.running = True
        self.status_label.config(text="🟢 En cours d'exécution")

    def pause(self):
        self.running = False
        self.status_label.config(text="🟡 En pause")

    def stop(self):
        self.running = False
        self.status_label.config(text="🔴 Arrêté")
        self.root.quit()  # Ferme l'interface graphique

    def launch(self):
        print("📢 Interface de contrôle en cours d'affichage...")
        self.root.mainloop()  # Démarre l'interface graphique
        time.sleep(1)  # Petite pause pour éviter la fermeture immédiate du thread
