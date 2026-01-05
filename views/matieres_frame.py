import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional
from models.matiere import Matiere
from utils.validators import valider_note, formater_note

class MatieresFrame(ttk.Frame):
    """
    Cadre affichant la liste des matières avec leurs notes et coefficients.
    """
    def __init__(self, parent, matieres: List[Matiere], on_note_change: Optional[Callable] = None):
        """
        Initialise le cadre des matières.
        
        Args:
            parent: Le widget parent
            matieres: Liste des matières à afficher
            on_note_change: Fonction à appeler quand une note est modifiée
        """
        super().__init__(parent)
        self.matieres = matieres
        self.on_note_change = on_note_change
        
        # Configuration du style
        self.style = ttk.Style()
        self.style.configure('Matiere.TFrame', background='#f0f0f0')
        self.style.configure('Matiere.TCheckbutton', background='#f0f0f0')
        
        # Création du canvas et de la barre de défilement
        self._creer_canvas_et_scrollbar()
        
        # Cadre pour les entêtes de colonnes
        self._creer_entetes_colonnes()
        
        # Cadre pour le contenu défilable
        self._creer_cadre_contenu()
        
        # Configurer la gestion du défilement
        self._configurer_defilement()
    
    def _creer_canvas_et_scrollbar(self):
        """Crée le canvas et la barre de défilement."""
        # Canvas pour le défilement
        self.canvas = tk.Canvas(
            self,
            borderwidth=0,
            highlightthickness=0,
            background='#f0f0f0'
        )
        
        # Barre de défilement verticale
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )
        
        # Configuration du canvas pour utiliser la barre de défilement
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Placement des widgets
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _creer_entetes_colonnes(self):
        """Crée les en-têtes de colonnes."""
        # Cadre pour les en-têtes
        header_frame = ttk.Frame(self, style='Matiere.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        # En-tête de la colonne de sélection
        ttk.Label(
            header_frame,
            text="Sélection",
            width=15,
            anchor=tk.CENTER,
            style='Header.TLabel'
        ).pack(side=tk.LEFT, padx=2)
        
        # En-tête de la colonne Matière
        ttk.Label(
            header_frame,
            text="Matière",
            width=25,
            anchor=tk.W,
            style='Header.TLabel'
        ).pack(side=tk.LEFT, padx=2)
        
        # En-tête de la colonne Coefficient
        ttk.Label(
            header_frame,
            text="Coeff.",
            width=10,
            anchor=tk.CENTER,
            style='Header.TLabel'
        ).pack(side=tk.LEFT, padx=2)
        
        # En-tête de la colonne Note
        ttk.Label(
            header_frame,
            text="Note / 20",
            width=15,
            anchor=tk.CENTER,
            style='Header.TLabel'
        ).pack(side=tk.LEFT, padx=2)
    
    def _creer_cadre_contenu(self):
        """Crée le cadre défilable contenant les matières."""
        # Cadre pour le contenu (sera placé dans le canvas)
        self.content_frame = ttk.Frame(self.canvas, style='Matiere.TFrame')
        self.content_id = self.canvas.create_window(
            (0, 0),
            window=self.content_frame,
            anchor=tk.NW
        )
        
        # Création des lignes pour chaque matière
        for i, matiere in enumerate(self.matieres):
            self._creer_ligne_matiere(matiere, i)
        
        # Mise à jour de la zone de défilement après l'ajout des widgets
        self.content_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def _creer_ligne_matiere(self, matiere: Matiere, index: int):
        """
        Crée une ligne pour une matière dans le tableau.
        
        Args:
            matiere: L'objet Matiere à afficher
            index: L'index de la ligne
        """
        # Cadre pour la ligne
        ligne_frame = ttk.Frame(self.content_frame, style='Matiere.TFrame')
        ligne_frame.pack(fill=tk.X, pady=2)
        
        # Case à cocher pour la sélection
        matiere.var = tk.BooleanVar(value=True)  # Par défaut, la matière est sélectionnée
        check = ttk.Checkbutton(
            ligne_frame,
            variable=matiere.var,
            style='Matiere.TCheckbutton'
        )
        check.pack(side=tk.LEFT, padx=2)
        
        # Nom de la matière
        ttk.Label(
            ligne_frame,
            text=matiere.nom,
            width=25,
            anchor=tk.W
        ).pack(side=tk.LEFT, padx=2)
        
        # Coefficient
        ttk.Label(
            ligne_frame,
            text=str(matiere.coefficient),
            width=10,
            anchor=tk.CENTER
        ).pack(side=tk.LEFT, padx=2)
        
        # Champ de saisie de la note
        self._creer_champ_note(ligne_frame, matiere)
    
    def _creer_champ_note(self, parent, matiere: Matiere):
        """
        Crée le champ de saisie pour une note.
        
        Args:
            parent: Le widget parent
            matiere: L'objet Matiere associé
        """
        # Validation de la saisie
        vcmd = (parent.register(
            lambda val: valider_note(val) or val == ""
        ), '%P')
        
        # Création du champ de saisie
        entry = ttk.Entry(
            parent,
            textvariable=matiere.note_var,
            width=10,
            justify=tk.CENTER,
            validate='key',
            validatecommand=vcmd
        )
        entry.pack(side=tk.LEFT, padx=2)
        
        # Lier l'événement de modification
        matiere.entry = entry
        if self.on_note_change:
            matiere.note_var.trace_add('write', self.on_note_change)
    
    def _configurer_defilement(self):
        """Configure la gestion du défilement du canvas."""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _on_frame_configure(event):
            # Ajuste la zone de défilement quand la taille du contenu change
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            # Ajuste la largeur du cadre de contenu à celle du canvas
            self.canvas.itemconfig(self.content_id, width=event.width)
        
        # Configuration des événements
        self.content_frame.bind("<Configure>", _on_frame_configure)
        self.canvas.bind("<Configure>", _on_frame_configure)
        
        # Activer le défilement avec la molette de la souris
        # Note: bind_all peut causer des fuites mémoire - utilisez bind à la place
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        self.canvas.bind("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # Linux scroll up
        self.canvas.bind("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))   # Linux scroll down
        
        # Désactiver la propagation des événements de la souris au cadre parent
        self.content_frame.bind('<Enter>', lambda e: self.canvas.bind('<MouseWheel>', _on_mousewheel))
        self.content_frame.bind('<Leave>', lambda e: self.canvas.unbind('<MouseWheel>'))
    
    def obtenir_matieres_selectionnees(self) -> List[Matiere]:
        """
        Retourne la liste des matières sélectionnées.
        
        Returns:
            List[Matiere]: Liste des matières sélectionnées
        """
        return [m for m in self.matieres if m.var.get()]
