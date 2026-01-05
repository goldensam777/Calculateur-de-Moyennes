#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calculateur de Moyenne - Application de calcul de moyenne scolaire
"""

import tkinter as tk
from tkinter import ttk, messagebox, StringVar
from typing import List, Optional

class Matiere:
    """
    A class to represent a school subject with its name, coefficient, and grade.
    """
    def __init__(self, nom: str, coefficient: float, note: float = 0.0):
        """
        Initialize a new subject.
        
        Args:
            nom (str): Name of the subject
            coefficient (float): Weight of the subject in average calculation
            note (float, optional): Default grade for the subject. Defaults to 0.0.
        """
        if coefficient <= 0:
            raise ValueError(f"Le coefficient doit être positif, reçu: {coefficient}")
        if not (0 <= note <= 20):
            raise ValueError(f"La note doit être entre 0 et 20, reçu: {note}")
            
        self.nom = nom
        self.coefficient = coefficient
        self.default_note = note
        self.note_var = StringVar(value=str(note))
        self.var = tk.BooleanVar()
        self.entry: Optional[ttk.Entry] = None

    @property
    def note(self) -> float:
        """Get the current grade as a float."""
        try:
            return float(self.note_var.get())
        except ValueError:
            return 0.0

    def __str__(self):
        return f"{self.nom} (coeff: {self.coefficient}, note: {self.note})"


class App:
    """Main application class that creates and manages the GUI."""
    
    def __init__(self, root):
        """Initialize the main application window."""
        self.root = root
        self.root.title("Calculateur de Moyenne")
        
        # Set window size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = screen_width // 2
        window_height = (screen_height * 3) // 4
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 4
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(400, 500)
        
        # Style configuration
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('TButton', font=('Arial', 10))
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = ttk.Label(
            self.main_frame, 
            text="Sélectionnez les matières à inclure dans la moyenne",
            style='Header.TLabel'
        )
        self.title_label.pack(pady=10)
        
        # Create scrollable frame for subjects
        self.create_matieres_frame()
        
        # Button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10, fill=tk.X)
        
        # Left button frame
        left_btn_frame = ttk.Frame(button_frame)
        left_btn_frame.pack(side='left', fill='x', expand=True)
        
        # Calculate button
        calc_btn = ttk.Button(
            left_btn_frame,
            text="Calculer la moyenne",
            command=self.calculer_moyenne
        )
        calc_btn.pack(side='left', padx=5)
        
        # Clear button
        clear_btn = ttk.Button(
            left_btn_frame,
            text="Effacer la sélection",
            command=self.clear_selection
        )
        clear_btn.pack(side='left', padx=5)
        
        # Add subject button
        add_btn = ttk.Button(
            button_frame,
            text="+ Ajouter une matière",
            command=self.ajouter_matiere_dialog
        )
        add_btn.pack(side='right', padx=5)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(
            self.main_frame,
            text="Résultats",
            padding=10
        )
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Initialize subjects
        self.matieres = [
            Matiere("Anglais", 2, 0.0),
            Matiere("Français", 2, 0.0),
            Matiere("Histoire-Géo", 2, 0.0),
            Matiere("Maths", 4, 0.0),
            Matiere("Philo", 2, 0.0),
            Matiere("PCT", 4, 0.0),
            Matiere("SVT", 5, 0.0)
        ]
        
        # Add subjects to frame
        self.add_matieres_to_frame()
    
    def create_matieres_frame(self):
        """Create a scrollable frame to hold the list of subjects."""
        self.canvas = tk.Canvas(self.main_frame, bg='white', highlightthickness=0)
        
        scrollbar = ttk.Scrollbar(
            self.main_frame, 
            orient="vertical",
            command=self.canvas.yview
        )
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def validate_note(self, new_value: str) -> bool:
        """Validate that the entered value is a number between 0 and 20."""
        if new_value == '':
            return True
        try:
            value = float(new_value)
            return 0 <= value <= 20
        except ValueError:
            return False

    def add_matieres_to_frame(self):
        """Add all subjects to the scrollable frame."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        for matiere in self.matieres:
            self.add_matiere_to_frame(matiere)
    
    def calculer_moyenne(self):
        """Calculate and display the weighted average of selected subjects."""
        selected = [m for m in self.matieres if m.var.get()]
        
        if not selected:
            messagebox.showwarning(
                "Aucune matière sélectionnée",
                "Veuillez sélectionner au moins une matière."
            )
            return
        
        # Validate notes
        invalid_notes = []
        for m in selected:
            try:
                note_val = float(m.note_var.get() or 0)
                if not (0 <= note_val <= 20):
                    invalid_notes.append(m.nom)
            except ValueError:
                invalid_notes.append(m.nom)
        
        if invalid_notes:
            messagebox.showerror(
                "Note(s) invalide(s)",
                f"Veuillez entrer des notes valides (entre 0 et 20) pour: {', '.join(invalid_notes)}"
            )
            return
        
        # Calculate weighted average
        try:
            somme_notes = sum(m.note * m.coefficient for m in selected)
            somme_coeffs = sum(m.coefficient for m in selected)
            moyenne = somme_notes / somme_coeffs
            
            # Clear previous results
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            # Display selected subjects
            ttk.Label(
                self.results_frame,
                text="Matières sélectionnées:",
                style='Header.TLabel'
            ).pack(anchor='w')
            
            for matiere in selected:
                ttk.Label(
                    self.results_frame,
                    text=f"- {matiere.nom}: Note = {matiere.note:.2f}, Coeff = {matiere.coefficient}"
                ).pack(anchor='w')
            
            # Display average with color coding
            avg_label = ttk.Label(
                self.results_frame,
                text=f"\nMoyenne pondérée: {moyenne:.2f}/20",
                style='Header.TLabel',
                foreground='green' if moyenne >= 10 else 'red'
            )
            avg_label.pack(pady=(10, 0), anchor='w')
            
            # Add comment based on average
            if moyenne >= 16:
                comment = "Excellent travail!"
                color = 'dark green'
            elif moyenne >= 14:
                comment = "Très bien!"
                color = 'green'
            elif moyenne >= 12:
                comment = "Bien!"
                color = 'blue'
            elif moyenne >= 10:
                comment = "Passable"
                color = 'orange'
            else:
                comment = "Doit faire des efforts"
                color = 'red'
                
            ttk.Label(
                self.results_frame,
                text=comment,
                foreground=color,
                font=('Arial', 10, 'italic')
            ).pack(pady=(5, 10), anchor='w')
            
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Une erreur est survenue lors du calcul: {str(e)}"
            )
    
    def ajouter_matiere_dialog(self):
        """Open a dialog to add a new subject."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Ajouter une matière")
        dialog.geometry("400x250")
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'400x250+{x}+{y}')
        
        # Form fields
        ttk.Label(dialog, text="Nom de la matière:", font=('Arial', 10)).pack(pady=(20, 5))
        nom_entry = ttk.Entry(dialog, width=30)
        nom_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Coefficient:", font=('Arial', 10)).pack(pady=(10, 5))
        coeff_var = tk.StringVar(value="1.0")
        coeff_entry = ttk.Spinbox(dialog, from_=0.5, to=10, increment=0.5, textvariable=coeff_var, width=10)
        coeff_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Note (sur 20):", font=('Arial', 10)).pack(pady=(10, 5))
        note_var = tk.StringVar(value="10.0")
        note_entry = ttk.Spinbox(dialog, from_=0, to=20, increment=0.5, textvariable=note_var, width=10)
        note_entry.pack(pady=5)
        
        def on_add():
            nom = nom_entry.get().strip()
            try:
                coeff = float(coeff_var.get())
                note = float(note_var.get())
                
                if not nom:
                    messagebox.showerror("Erreur", "Veuillez entrer un nom de matière.")
                    return
                if coeff <= 0:
                    messagebox.showerror("Erreur", "Le coefficient doit être supérieur à 0.")
                    return
                if not (0 <= note <= 20):
                    messagebox.showerror("Erreur", "La note doit être comprise entre 0 et 20.")
                    return
                
                self.ajouter_matiere(nom, coeff, note)
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Annuler", command=dialog.destroy).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Ajouter", command=on_add).pack(side='left', padx=10)
        
        nom_entry.focus_set()
    
    def ajouter_matiere(self, nom: str, coefficient: float, note: float):
        """Add a new subject to the list and update the UI."""
        nouvelle_matiere = Matiere(nom, coefficient, note)
        self.matieres.append(nouvelle_matiere)
        self.add_matiere_to_frame(nouvelle_matiere)
        self.canvas.yview_moveto(1.0)
    
    def add_matiere_to_frame(self, matiere: Matiere):
        """Add a single subject's UI elements to the scrollable frame."""
        frame = ttk.Frame(self.scrollable_frame)
        frame.pack(fill='x', pady=2, padx=5)
        
        # Checkbox for selection
        cb = ttk.Checkbutton(
            frame,
            text=f"{matiere.nom} (Coeff: {matiere.coefficient}):",
            variable=matiere.var,
            onvalue=True,
            offvalue=False
        )
        cb.pack(side='left')
        
        # Entry for note input
        vcmd = (frame.register(self.validate_note), '%P')
        entry = ttk.Entry(
            frame,
            textvariable=matiere.note_var,
            width=5,
            validate='key',
            validatecommand=vcmd
        )
        entry.pack(side='left', padx=5)
        ttk.Label(frame, text="/20").pack(side='left')
        
        matiere.entry = entry
        
        # Delete button
        delete_btn = ttk.Button(
            frame,
            text="×",
            width=2,
            command=lambda m=matiere, f=frame: self.supprimer_matiere(m, f)
        )
        delete_btn.pack(side='right', padx=5)
    
    def supprimer_matiere(self, matiere: Matiere, frame: ttk.Frame):
        """Remove a subject from the list."""
        if messagebox.askyesno(
            "Confirmer la suppression",
            f"Voulez-vous vraiment supprimer la matière '{matiere.nom}'?"
        ):
            self.matieres.remove(matiere)
            frame.destroy()
    
    def clear_selection(self):
        """Uncheck all checkboxes and clear results."""
        for matiere in self.matieres:
            matiere.var.set(False)
        
        for widget in self.results_frame.winfo_children():
            widget.destroy()


def main():
    """Entry point of the application."""
    try:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()