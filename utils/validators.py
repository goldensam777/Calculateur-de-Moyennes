def valider_note(nouvelle_valeur: str) -> bool:
    """
    Valide que la valeur entrée est un nombre entre 0 et 20.
    
    Args:
        nouvelle_valeur: La valeur à valider
        
    Returns:
        bool: True si la valeur est valide, False sinon
    """
    if not nouvelle_valeur:  # Permet de vider le champ
        return True
        
    try:
        valeur = float(nouvelle_valeur.replace(',', '.'))
        return 0 <= valeur <= 20
    except ValueError:
        return False

def formater_note(valeur: str) -> str:
    """
    Formate la note pour affichage (remplace le point par une virgule).
    
    Args:
        valeur: La valeur à formater
        
    Returns:
        str: La valeur formatée
    """
    return valeur.replace('.', ',') if valeur else ""
