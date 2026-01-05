import tkinter as tk
from tkinter import messagebox
from typing import List
from CM.models.matiere import Matiere
from CM.views.main_window import MainWindow
from CM.views.matieres_frame import MatieresFrame
from CM.utils.calculs import calculer_moyenne, calculer_moyenne_generale

class CalculateurMoyenneController:
    """
    Contrôleur principal de l'application.
    Gère les interactions entre les vues et les modèles.
    """
    def __init__(self):
        # Liste des matières avec leurs coefficients par défaut
        self.matieres = [
            Matiere("Mathématiques", 7),
            Matiere("Physique-Chimie", 6),
            Matiere("SVT", 6),
            Matiere("Français", 5),
            Matiere("Philosophie", 4),
            Matiere("Histoire-Géographie", 3),
            Matiere("Anglais", 3),
            Matiere("Espagnol", 2),
            Matiere("EPS", 2),
            Matiere("Spécialité 1", 16),
            Matiere("Spécialité 2", 16),
            Matiere("Grand Oral", 10)
        ]
        
        # Initialisation de l'interface graphique
        self.root = tk.Tk()
        self.main_window = MainWindow(
            self.root,
            on_calculer_click=self.calculer_moyenne,
            on_reset_click=self.reinitialiser_notes
        )
        
        # Création du cadre des matières
        self.creer_cadre_matieres()
    
    def creer_cadre_matieres(self):
        """Crée et affiche le cadre des matières."""
        matieres_frame = MatieresFrame(
            self.main_window.main_frame,
            self.matieres,
            on_note_change=self.on_note_change
        )
        self.main_window.definir_cadre_matieres(matieres_frame)
    
    def on_note_change(self, *args):
        """Appelée lorsqu'une note est modifiée."""
        # Pourrait être utilisé pour une mise à jour en temps réel si nécessaire
        pass
    
    def calculer_moyenne(self):
        """Calcule et affiche la moyenne des matières sélectionnées."""
        # Récupérer les matières sélectionnées
        matieres_frame = self.main_window.matieres_frame
        matieres_selectionnees = matieres_frame.obtenir_matieres_selectionnees()
        
        if not matieres_selectionnees:
            messagebox.showwarning(
                "Aucune matière sélectionnée",
                "Veuillez sélectionner au moins une matière pour calculer la moyenne."
            )
            return
        
        # Calculer la moyenne
        moyenne = calculer_moyenne(matieres_selectionnees)
        
        # Afficher le résultat
        self.main_window.afficher_resultat(moyenne)
    
    def calculer_moyenne_generale(self):
        """Calcule et affiche la moyenne générale de toutes les matières."""
        moyenne = calculer_moyenne_generale(self.matieres)
        self.main_window.afficher_resultat(moyenne, est_moyenne_generale=True)
    
    def reinitialiser_notes(self):
        """Réinitialise toutes les notes à leurs valeurs par défaut."""
        for matiere in self.matieres:
            matiere.note_var.set(str(matiere.default_note))
        
        # Mettre à jour l'affichage
        self.main_window.afficher_resultat(0.0)
    
    def run(self):
        """Lance l'application."""
        # Essayer de définir l'icône de l'application (Windows uniquement)
        try:
            from ctypes import windll
            windll.shell32.SetCurrentProcessExplicitAppUserModelID("CalculateurMoyenne")
            self.root.iconbitmap("CM.ico")
        except (ImportError, AttributeError, FileNotFoundError):
            # ImportError: windll non disponible (non-Windows)
            # AttributeError: shell32 non disponible
            # FileNotFoundError: icône non trouvée
            pass
        
        self.root.mainloop()

if __name__ == "__main__":
    app = CalculateurMoyenneController()
    app.run()
