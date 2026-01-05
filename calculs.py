"""
Module de calcul partagé entre les différentes versions (Tkinter, Flask, Kivy)
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Matiere:
    """Classe représentant une matière avec son coefficient et sa note."""
    nom: str
    coefficient: float
    note: float = 0.0
    
    def __post_init__(self):
        """Valider les données lors de la création."""
        if self.coefficient <= 0:
            raise ValueError(f"Le coefficient doit être positif, reçu: {self.coefficient}")
        if not (0 <= self.note <= 20):
            raise ValueError(f"La note doit être entre 0 et 20, reçu: {self.note}")


def calculer_moyenne(matieres: List[Matiere]) -> float:
    """
    Calcule la moyenne pondérée des matières.
    
    Args:
        matieres: Liste des matières sélectionnées
        
    Returns:
        La moyenne pondérée
    """
    if not matieres:
        return 0.0
    
    somme_notes = sum(m.note * m.coefficient for m in matieres)
    somme_coeffs = sum(m.coefficient for m in matieres)
    
    return somme_notes / somme_coeffs if somme_coeffs > 0 else 0.0


def obtenir_appreciation(moyenne: float) -> dict:
    """
    Retourne l'appréciation et la couleur en fonction de la moyenne.
    
    Args:
        moyenne: La moyenne calculée
        
    Returns:
        Un dictionnaire avec le commentaire et la couleur
    """
    if moyenne >= 16:
        return {"texte": "Excellent travail!", "couleur": "#27ae60"}
    elif moyenne >= 14:
        return {"texte": "Très bien!", "couleur": "#2ecc71"}
    elif moyenne >= 12:
        return {"texte": "Bien!", "couleur": "#3498db"}
    elif moyenne >= 10:
        return {"texte": "Passable", "couleur": "#f39c12"}
    else:
        return {"texte": "Doit faire des efforts", "couleur": "#e74c3c"}


def valider_note(note_str: str) -> bool:
    """Valide qu'une note est un nombre entre 0 et 20."""
    if not note_str:
        return True
    try:
        note = float(note_str)
        return 0 <= note <= 20
    except ValueError:
        return False
