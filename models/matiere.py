from tkinter import StringVar, ttk
from typing import Optional

class Matiere:
    """
    A class to represent a school subject with its name, coefficient, and grade.
    This class handles the data and UI elements for each subject.
    """
    def __init__(self, nom: str, coefficient: float, note: float = 0.0):
        """
        Initialize a new subject.
        
        Args:
            nom (str): Name of the subject
            coefficient (float): Weight of the subject in average calculation
            note (float, optional): Default grade for the subject. Defaults to 0.0.
            
        Raises:
            ValueError: Si le coefficient est négatif ou nul
            ValueError: Si la note est en dehors de [0, 20]
        """
        if coefficient <= 0:
            raise ValueError(f"Le coefficient doit être positif, reçu: {coefficient}")
        if not (0 <= note <= 20):
            raise ValueError(f"La note doit être entre 0 et 20, reçu: {note}")
            
        self.nom = nom  # Subject name (e.g., 'Maths', 'Physics')
        self.coefficient = coefficient  # Weight of the subject (e.g., 2.0, 1.5)
        self.default_note = note  # Store the default note for reference
        self.note_var = StringVar(value=str(note))  # Tkinter variable to track grade input
        self.var = None  # Will be set by the UI component
        self.entry: Optional[ttk.Entry] = None  # Will hold the grade entry widget

    @property
    def note(self) -> float:
        """
        Property to get the current grade as a float.
        Returns 0.0 if the input is not a valid number.
        """
        try:
            return float(self.note_var.get())
        except ValueError:
            return 0.0  # Return 0 if the input is not a valid number

    def __str__(self):
        return f"{self.nom} (coeff: {self.coefficient}, note: {self.note})"
