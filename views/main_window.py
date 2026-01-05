import tkinter as tk
from tkinter import ttk
from typing import List, Callable
from models.matiere import Matiere

class MainWindow:
    """
    Classe principale de la fenêtre de l'application.
    Gère la mise en page et les interactions principales.
    """
    def __init__(self, root, on_calculer_click: Callable, on_reset_click: Callable):
        """
        Initialise la fenêtre principale.
        
        Args:
            root: La fenêtre racine Tkinter
            on_calculer_click: Fonction à appeler lors du clic sur le bouton Calculer
            on_reset_click: Fonction à appeler lors du clic sur le bouton Réinitialiser
        """
        self.root = root
        self.root.title("Calculateur de Moyenne")  # Titre de la fenêtre
        
        # Configuration de la taille de la fenêtre
        self._configurer_taille_fenetre()
        
        # Configuration du style
        self._configurer_styles()
        
        # Création du conteneur principal
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        self.title_label = ttk.Label(
            self.main_frame, 
            text="Sélectionnez les matières à inclure dans la moyenne",
            style='Header.TLabel'
        )
        self.title_label.pack(pady=10)
        
        # Cadre pour la liste des matières (sera défini par le contrôleur)
        self.matieres_frame = None
        
        # Cadre des boutons
        self._creer_cadre_boutons(on_calculer_click, on_reset_click)
        
        # Étiquette pour afficher le résultat
        self.resultat_var = tk.StringVar()
        self.resultat_label = ttk.Label(
            self.main_frame, 
            textvariable=self.resultat_var,
            style='Resultat.TLabel'
        )
        self.resultat_label.pack(pady=10)
    
    def _configurer_taille_fenetre(self):
        """Configure la taille et la position de la fenêtre."""
        # Taille de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Taille de la fenêtre (1/2 largeur, 3/4 hauteur)
        window_width = screen_width // 2
        window_height = (screen_height * 3) // 4
        
        # Position pour centrer la fenêtre
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 4
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(400, 500)  # Taille minimale
    
    def _configurer_styles(self):
        """Configure les styles de l'interface utilisateur."""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Resultat.TLabel', font=('Arial', 12, 'bold'), foreground='blue')
    
    def _creer_cadre_boutons(self, on_calculer_click, on_reset_click):
        """Crée le cadre contenant les boutons principaux."""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10, fill=tk.X)
        
        # Bouton Calculer
        self.calculer_btn = ttk.Button(
            button_frame, 
            text="Calculer la moyenne",
            command=on_calculer_click
        )
        self.calculer_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Bouton Réinitialiser
        self.reset_btn = ttk.Button(
            button_frame, 
            text="Réinitialiser",
            command=on_reset_click
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
    
    def definir_cadre_matieres(self, matieres_frame):
        """Définit le cadre des matières."""
        if self.matieres_frame:
            self.matieres_frame.pack_forget()
        
        self.matieres_frame = matieres_frame
        self.matieres_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def afficher_resultat(self, moyenne: float, est_moyenne_generale: bool = False):
        """
        Affiche le résultat du calcul de la moyenne.
        
        Args:
            moyenne: La moyenne calculée
            est_moyenne_generale: Si True, affiche la mention "Moyenne générale"
        """
        if est_moyenne_generale:
            texte = f"Moyenne générale: {moyenne:.2f}"
        else:
            texte = f"Moyenne: {moyenne:.2f}"
        
        # Mise à jour du texte et du style en fonction de la moyenne
        self.resultat_var.set(texte)
        
        style = ttk.Style()
        if moyenne < 10:
            style.configure('Resultat.TLabel', foreground='red')
        elif moyenne < 12:
            style.configure('Resultat.TLabel', foreground='orange')
        else:
            style.configure('Resultat.TLabel', foreground='green')
