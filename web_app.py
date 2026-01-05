#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Version Web du Calculateur de Moyenne avec Flask
Accessible depuis : http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from calculs import Matiere, calculer_moyenne, obtenir_appreciation, valider_note
import json

app = Flask(__name__)

# Matières par défaut
MATIERES_PAR_DEFAUT = [
    {"nom": "Anglais", "coefficient": 2},
    {"nom": "Français", "coefficient": 2},
    {"nom": "Histoire-Géo", "coefficient": 2},
    {"nom": "Maths", "coefficient": 4},
    {"nom": "Philo", "coefficient": 2},
    {"nom": "Physique-Chimie", "coefficient": 4},
    {"nom": "SVT", "coefficient": 5},
]


@app.route('/')
def index():
    """Page d'accueil."""
    return render_template('index.html', matieres=MATIERES_PAR_DEFAUT)


@app.route('/api/calculer', methods=['POST'])
def calculer():
    """API pour calculer la moyenne."""
    try:
        donnees = request.json
        
        # Valider les données reçues
        if not donnees or 'matieres' not in donnees:
            return jsonify({"error": "Données invalides"}), 400
        
        # Construire la liste des matières sélectionnées
        matieres_selectionnees = []
        for m in donnees['matieres']:
            if m['selectionnee']:
                try:
                    note = float(m['note']) if m['note'] else 0.0
                    if not (0 <= note <= 20):
                        return jsonify({"error": f"Note invalide pour {m['nom']}"}), 400
                    
                    matiere = Matiere(nom=m['nom'], coefficient=m['coefficient'], note=note)
                    matieres_selectionnees.append(matiere)
                except (ValueError, KeyError) as e:
                    return jsonify({"error": f"Erreur pour {m['nom']}: {str(e)}"}), 400
        
        if not matieres_selectionnees:
            return jsonify({"error": "Veuillez sélectionner au moins une matière"}), 400
        
        # Calculer la moyenne
        moyenne = calculer_moyenne(matieres_selectionnees)
        appreciation = obtenir_appreciation(moyenne)
        
        return jsonify({
            "moyenne": round(moyenne, 2),
            "appreciation": appreciation['texte'],
            "couleur": appreciation['couleur'],
            "matieres": [
                {
                    "nom": m.nom,
                    "note": m.note,
                    "coefficient": m.coefficient
                }
                for m in matieres_selectionnees
            ]
        })
    
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500


@app.route('/api/matieres', methods=['GET'])
def get_matieres():
    """Récupère la liste des matières par défaut."""
    return jsonify(MATIERES_PAR_DEFAUT)


@app.route('/api/ajouter-matiere', methods=['POST'])
def ajouter_matiere():
    """Ajoute une nouvelle matière."""
    try:
        donnees = request.json
        
        nom = donnees.get('nom', '').strip()
        coefficient = float(donnees.get('coefficient', 1))
        
        if not nom:
            return jsonify({"error": "Le nom est requis"}), 400
        if coefficient <= 0:
            return jsonify({"error": "Le coefficient doit être > 0"}), 400
        
        # Valider que ce n'est pas déjà dans les matieres par défaut
        if any(m['nom'].lower() == nom.lower() for m in MATIERES_PAR_DEFAUT):
            return jsonify({"error": "Cette matière existe déjà"}), 400
        
        MATIERES_PAR_DEFAUT.append({"nom": nom, "coefficient": coefficient})
        
        return jsonify({
            "success": True,
            "matiere": {"nom": nom, "coefficient": coefficient}
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
