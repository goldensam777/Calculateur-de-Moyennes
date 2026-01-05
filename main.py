#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calculateur de Moyenne - Application de calcul de moyenne scolaire
"""

import sys
import os

# Ajouter le répertoire parent si le script n'est pas lancé depuis le bon chemin
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller import CalculateurMoyenneController

def main():
    """Point d'entrée principal de l'application."""
    try:
        # Création et démarrage de l'application
        app = CalculateurMoyenneController()
        app.run()
    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        
        # Afficher une boîte de dialogue d'erreur en cas de problème
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale
        
        messagebox.showerror(
            "Erreur",
            f"Une erreur est survenue :\n{str(e)}\n\n"
            "Veuillez réessayer ou contacter le support si le problème persiste."
        )
        
        # Afficher la trace complète dans la console pour le débogage
        import traceback
        traceback.print_exc()
        
        # Attendre que l'utilisateur ferme la boîte de dialogue
        root.destroy()

if __name__ == "__main__":
    main()