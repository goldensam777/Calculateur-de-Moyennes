#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Version Mobile du Calculateur de Moyenne avec Kivy
Fonctionne sur Android et iOS
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.image import Image
from calculs import Matiere, calculer_moyenne, obtenir_appreciation
from datetime import datetime
import json
import os

# Configuration de la fenêtre
Window.size = (400, 800)


class MatiereItem(BoxLayout):
    """Widget représentant une matière."""
    
    def __init__(self, matiere, on_delete=None, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, height=80, **kwargs)
        self.matiere = matiere
        self.on_delete = on_delete
        self.padding = 5
        self.spacing = 5
        
        # Ligne 1 : Checkbox et nom
        line1 = BoxLayout(size_hint_y=0.5)
        self.checkbox = CheckBox(size_hint_x=0.1, active=True)
        self.checkbox.bind(active=self.on_checkbox)
        line1.add_widget(self.checkbox)
        
        info = BoxLayout(orientation='vertical', size_hint_x=0.75)
        info.add_widget(Label(text=matiere.nom, size_hint_y=0.5, bold=True))
        info.add_widget(Label(text=f"Coeff: {matiere.coefficient}", size_hint_y=0.5, size=12))
        line1.add_widget(info)
        
        delete_btn = Button(text="×", size_hint_x=0.15, background_color=(1, 0, 0, 0.7))
        delete_btn.bind(on_press=self.on_delete_click)
        line1.add_widget(delete_btn)
        
        # Ligne 2 : Saisie note
        line2 = BoxLayout(size_hint_y=0.5)
        line2.add_widget(Label(text="Note:", size_hint_x=0.2))
        self.note_input = TextInput(
            text="0",
            multiline=False,
            input_filter='float',
            size_hint_x=0.5
        )
        line2.add_widget(self.note_input)
        line2.add_widget(Label(text="/20", size_hint_x=0.3))
        
        self.add_widget(line1)
        self.add_widget(line2)
    
    def on_checkbox(self, checkbox, value):
        """Appelé quand la checkbox change."""
        pass
    
    def on_delete_click(self, instance):
        """Appelé quand on clique sur le bouton supprimer."""
        if self.on_delete:
            self.on_delete(self.matiere)
    
    def get_note(self):
        """Récupère la note saisie."""
        try:
            return float(self.note_input.text) if self.note_input.text else 0.0
        except ValueError:
            return 0.0
    
    def is_selected(self):
        """Vérifie si la matière est sélectionnée."""
        return self.checkbox.active


class CalculateurApp(App):
    """Application principal du calculateur."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.matiere_items = []
        self.matieres_par_defaut = [
            Matiere("Anglais", 2),
            Matiere("Français", 2),
            Matiere("Histoire-Géo", 2),
            Matiere("Maths", 4),
            Matiere("Philo", 2),
            Matiere("Physique-Chimie", 4),
            Matiere("SVT", 5),
        ]
    
    def build(self):
        """Construire l'interface de l'app."""
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint_y=0.1, orientation='vertical')
        header.add_widget(Label(text="📊 Calculateur de Moyenne", size=24, bold=True))
        header.add_widget(Label(text="Calculez votre moyenne pondérée", size=12))
        root.add_widget(header)
        
        # Matières (scrollable)
        self.matieres_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.matieres_layout.bind(minimum_height=self.matieres_layout.setter('height'))
        
        scroll = ScrollView(size_hint=(1, 0.6))
        scroll.add_widget(self.matieres_layout)
        root.add_widget(scroll)
        
        # Afficher les matières par défaut
        for matiere in self.matieres_par_defaut:
            self.ajouter_matiere_item(matiere)
        
        # Boutons
        buttons_layout = BoxLayout(size_hint_y=0.15, spacing=5)
        
        btn_calculer = Button(text="Calculer", background_color=(0.3, 0.7, 1, 1))
        btn_calculer.bind(on_press=self.calculer)
        buttons_layout.add_widget(btn_calculer)
        
        btn_reset = Button(text="Réinitialiser", background_color=(0.7, 0.7, 0.7, 1))
        btn_reset.bind(on_press=self.reinitialiser)
        buttons_layout.add_widget(btn_reset)
        
        btn_ajouter = Button(text="+ Ajouter", background_color=(0.2, 0.8, 0.3, 1))
        btn_ajouter.bind(on_press=self.ouvrir_modal_ajouter)
        buttons_layout.add_widget(btn_ajouter)
        
        root.add_widget(buttons_layout)
        
        # Résultats
        self.resultats_layout = BoxLayout(orientation='vertical', size_hint_y=0.15, padding=10)
        root.add_widget(self.resultats_layout)
        
        return root
    
    def ajouter_matiere_item(self, matiere):
        """Ajouter un widget matière à l'interface."""
        item = MatiereItem(matiere, on_delete=self.supprimer_matiere)
        self.matiere_items.append(item)
        self.matieres_layout.add_widget(item)
    
    def supprimer_matiere(self, matiere):
        """Supprimer une matière."""
        self.matiere_items = [item for item in self.matiere_items if item.matiere != matiere]
        self.matieres_layout.clear_widgets()
        for item in self.matiere_items:
            self.matieres_layout.add_widget(item)
    
    def calculer(self, instance):
        """Calculer la moyenne."""
        matieres_selectionnees = []
        
        for item in self.matiere_items:
            if item.is_selected():
                note = item.get_note()
                try:
                    m = Matiere(item.matiere.nom, item.matiere.coefficient, note)
                    matieres_selectionnees.append(m)
                except ValueError as e:
                    self.afficher_erreur(str(e))
                    return
        
        if not matieres_selectionnees:
            self.afficher_erreur("Veuillez sélectionner au moins une matière")
            return
        
        moyenne = calculer_moyenne(matieres_selectionnees)
        appreciation = obtenir_appreciation(moyenne)
        
        self.afficher_resultats(moyenne, appreciation, matieres_selectionnees)
    
    def afficher_resultats(self, moyenne, appreciation, matieres):
        """Afficher les résultats."""
        self.resultats_layout.clear_widgets()
        
        # Score
        texte_moyenne = f"Moyenne: {moyenne:.2f}/20"
        self.resultats_layout.add_widget(
            Label(text=texte_moyenne, size=18, bold=True, color=self.hex_to_rgb(appreciation['couleur']))
        )
        
        # Appréciation
        self.resultats_layout.add_widget(
            Label(text=appreciation['texte'], size=14, italic=True)
        )
    
    def afficher_erreur(self, message):
        """Afficher un message d'erreur."""
        self.resultats_layout.clear_widgets()
        self.resultats_layout.add_widget(Label(text=f"❌ {message}", color=(1, 0, 0, 1)))
    
    def reinitialiser(self, instance):
        """Réinitialiser les champs."""
        for item in self.matiere_items:
            item.note_input.text = "0"
        self.resultats_layout.clear_widgets()
    
    def ouvrir_modal_ajouter(self, instance):
        """Ouvrir un modal pour ajouter une matière."""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(text="Nom:", size_hint_y=0.2))
        nom_input = TextInput(multiline=False, size_hint_y=0.2)
        content.add_widget(nom_input)
        
        content.add_widget(Label(text="Coefficient:", size_hint_y=0.2))
        coeff_input = TextInput(text="1", multiline=False, input_filter='float', size_hint_y=0.2)
        content.add_widget(coeff_input)
        
        buttons = BoxLayout(size_hint_y=0.2, spacing=5)
        
        def ajouter():
            nom = nom_input.text.strip()
            try:
                coeff = float(coeff_input.text)
                if not nom or coeff <= 0:
                    self.afficher_erreur("Données invalides")
                    popup.dismiss()
                    return
                
                self.ajouter_matiere_item(Matiere(nom, coeff))
                popup.dismiss()
            except ValueError:
                self.afficher_erreur("Veuillez entrer des nombres valides")
                popup.dismiss()
        
        btn_ajouter = Button(text="Ajouter")
        btn_ajouter.bind(on_press=lambda x: ajouter())
        buttons.add_widget(btn_ajouter)
        
        btn_annuler = Button(text="Annuler")
        buttons.add_widget(btn_annuler)
        
        content.add_widget(buttons)
        
        popup = Popup(title="Ajouter une matière", content=content, size_hint=(0.9, 0.6))
        btn_annuler.bind(on_press=popup.dismiss)
        popup.open()
    
    @staticmethod
    def hex_to_rgb(hex_color):
        """Convertir couleur hex en RGB Kivy."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4)) + (1,)


if __name__ == '__main__':
    CalculateurApp().run()
