#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Version Web du Calculateur de Moyenne avec Flask et SQLite
Accessible depuis : http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from calculs import Matiere, calculer_moyenne, obtenir_appreciation, valider_note
import sqlite3
import json
import os
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'profils.db'

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


def init_db():
    """Initialiser la base de données."""
    if os.path.exists(DB_FILE):
        return
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Table pour les profils
    c.execute('''
        CREATE TABLE profils (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE NOT NULL,
            donnees TEXT NOT NULL,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table pour l'historique
    c.execute('''
        CREATE TABLE historique (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profil_id INTEGER,
            moyenne REAL,
            date_calcul TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(profil_id) REFERENCES profils(id)
        )
    ''')
    
    conn.commit()
    conn.close()


def get_db():
    """Obtenir une connexion à la base de données."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    """Page d'accueil."""
    return render_template('index.html', matieres=MATIERES_PAR_DEFAUT)


@app.route('/api/calculer', methods=['POST'])
def calculer():
    """API pour calculer la moyenne."""
    try:
        donnees = request.json
        
        if not donnees or 'matieres' not in donnees:
            return jsonify({"error": "Données invalides"}), 400
        
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
        
        if any(m['nom'].lower() == nom.lower() for m in MATIERES_PAR_DEFAUT):
            return jsonify({"error": "Cette matière existe déjà"}), 400
        
        MATIERES_PAR_DEFAUT.append({"nom": nom, "coefficient": coefficient})
        
        return jsonify({
            "success": True,
            "matiere": {"nom": nom, "coefficient": coefficient}
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============ ENDPOINTS DE SAUVEGARDE ============

@app.route('/api/profils', methods=['GET'])
def lister_profils():
    """Lister tous les profils sauvegardés."""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, nom, date_modification FROM profils ORDER BY date_modification DESC')
        profils = [dict(row) for row in c.fetchall()]
        conn.close()
        return jsonify(profils)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/profils', methods=['POST'])
def creer_profil():
    """Créer un nouveau profil."""
    try:
        donnees = request.json
        nom = donnees.get('nom', '').strip()
        matieres_data = donnees.get('matieres', [])
        
        if not nom:
            return jsonify({"error": "Le nom du profil est requis"}), 400
        
        conn = get_db()
        c = conn.cursor()
        
        try:
            c.execute(
                'INSERT INTO profils (nom, donnees) VALUES (?, ?)',
                (nom, json.dumps(matieres_data))
            )
            conn.commit()
            profil_id = c.lastrowid
            
            return jsonify({
                "success": True,
                "id": profil_id,
                "nom": nom
            })
        except sqlite3.IntegrityError:
            return jsonify({"error": f"Un profil nommé '{nom}' existe déjà"}), 400
        finally:
            conn.close()
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/profils/<int:profil_id>', methods=['GET'])
def charger_profil(profil_id):
    """Charger un profil existant."""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, nom, donnees FROM profils WHERE id = ?', (profil_id,))
        row = c.fetchone()
        conn.close()
        
        if not row:
            return jsonify({"error": "Profil non trouvé"}), 404
        
        return jsonify({
            "id": row['id'],
            "nom": row['nom'],
            "matieres": json.loads(row['donnees'])
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/profils/<int:profil_id>', methods=['PUT'])
def mettre_a_jour_profil(profil_id):
    """Mettre à jour un profil existant."""
    try:
        donnees = request.json
        matieres_data = donnees.get('matieres', [])
        
        conn = get_db()
        c = conn.cursor()
        c.execute(
            'UPDATE profils SET donnees = ?, date_modification = CURRENT_TIMESTAMP WHERE id = ?',
            (json.dumps(matieres_data), profil_id)
        )
        conn.commit()
        
        if c.rowcount == 0:
            return jsonify({"error": "Profil non trouvé"}), 404
        
        conn.close()
        
        return jsonify({"success": True, "id": profil_id})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/profils/<int:profil_id>', methods=['DELETE'])
def supprimer_profil(profil_id):
    """Supprimer un profil."""
    try:
        conn = get_db()
        c = conn.cursor()
        
        # Supprimer d'abord l'historique
        c.execute('DELETE FROM historique WHERE profil_id = ?', (profil_id,))
        
        # Puis le profil
        c.execute('DELETE FROM profils WHERE id = ?', (profil_id,))
        conn.commit()
        
        if c.rowcount == 0:
            return jsonify({"error": "Profil non trouvé"}), 404
        
        conn.close()
        
        return jsonify({"success": True})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/historique/<int:profil_id>', methods=['GET'])
def obtenir_historique(profil_id):
    """Obtenir l'historique des calculs pour un profil."""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            SELECT id, moyenne, date_calcul 
            FROM historique 
            WHERE profil_id = ? 
            ORDER BY date_calcul DESC 
            LIMIT 50
        ''', (profil_id,))
        historique = [dict(row) for row in c.fetchall()]
        conn.close()
        
        return jsonify(historique)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/historique', methods=['POST'])
def ajouter_historique():
    """Ajouter une entrée à l'historique."""
    try:
        donnees = request.json
        profil_id = donnees.get('profil_id')
        moyenne = donnees.get('moyenne')
        
        if profil_id is None or moyenne is None:
            return jsonify({"error": "Données invalides"}), 400
        
        conn = get_db()
        c = conn.cursor()
        c.execute(
            'INSERT INTO historique (profil_id, moyenne) VALUES (?, ?)',
            (profil_id, moyenne)
        )
        conn.commit()
        conn.close()
        
        return jsonify({"success": True})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
