from typing import List
from CM.models.matiere import Matiere

def calculer_moyenne(matieres: List[Matiere]) -> float:
    """
    Calcule la moyenne pondérée des matières sélectionnées.
    
    Args:
        matieres: Liste des matières à inclure dans le calcul
        
    Returns:
        float: La moyenne pondérée
    """
    total_notes = 0.0
    total_coefficients = 0.0
    
    for matiere in matieres:
        # Vérifie si la matière est sélectionnée (var peut être None au démarrage)
        if matiere.var and matiere.var.get():
            total_notes += matiere.note * matiere.coefficient
            total_coefficients += matiere.coefficient
    
    return total_notes / total_coefficients if total_coefficients > 0 else 0.0

def calculer_moyenne_generale(toutes_les_matieres: List[Matiere]) -> float:
    """
    Calcule la moyenne générale de toutes les matières.
    
    Args:
        toutes_les_matieres: Liste de toutes les matières
        
    Returns:
        float: La moyenne générale
    """
    total_notes = 0.0
    total_coefficients = 0.0
    
    for matiere in toutes_les_matieres:
        total_notes += matiere.note * matiere.coefficient
        total_coefficients += matiere.coefficient
    
    return total_notes / total_coefficients if total_coefficients > 0 else 0.0
