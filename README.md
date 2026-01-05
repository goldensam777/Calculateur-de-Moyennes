# Calculateur de Moyenne 📊

Une application Python moderne pour calculer les moyennes scolaires avec une interface graphique intuitive et professionnelle.

## ✨ Fonctionnalités

- ✅ **Calcul de moyenne pondérée** - Calcule automatiquement la moyenne en fonction des coefficients
- ✅ **Sélection flexible** - Choisissez les matières à inclure/exclure du calcul
- ✅ **Validation des entrées** - Vérification en temps réel des notes (0-20)
- ✅ **Interface réactive** - Affichage immédiat des résultats avec couleurs (rouge/orange/vert)
- ✅ **Réinitialisation** - Bouton pour remettre toutes les notes à zéro
- ✅ **Liste défilable** - Support de nombreuses matières avec scrollbar

## 📋 Prérequis

- **Python 3.6+**
- **Tkinter** (inclus avec Python sur la plupart des systèmes)

Pour vérifier si Tkinter est installé :
```bash
python -m tkinter
```

## 🚀 Installation

### Option 1 : Cloner depuis GitHub
```bash
git clone https://github.com/votre-username/calculateur-moyenne.git
cd calculateur-moyenne
```

### Option 2 : Créer un environnement virtuel (recommandé)
```bash
python -m venv venv

# Sur Linux/Mac :
source venv/bin/activate

# Sur Windows :
venv\Scripts\activate

# Puis lancer l'application
python main.py
```

## 🎮 Utilisation

1. Lancez l'application :
   ```bash
   python main.py
   ```

2. La fenêtre s'ouvre avec la liste de toutes les matières

3. Saisissez vos notes (0-20) dans les champs de saisie

4. Cochez/décochez les matières à inclure dans la moyenne

5. Cliquez sur "**Calculer la moyenne**" pour voir le résultat

6. La couleur du résultat change selon la note :
   - 🔴 **Rouge** : < 10
   - 🟠 **Orange** : 10-12
   - 🟢 **Vert** : ≥ 12

## 📁 Structure du Projet

```
calculateur-moyenne/
├── models/
│   ├── __init__.py
│   └── matiere.py          # Classe Matiere (données)
├── views/
│   ├── __init__.py
│   ├── main_window.py      # Fenêtre principale
│   └── matieres_frame.py   # Affichage des matières
├── utils/
│   ├── __init__.py
│   ├── calculs.py          # Logique de calcul
│   └── validators.py       # Validation des entrées
├── main.py                 # Point d'entrée
├── controller.py           # Contrôleur (MVC)
├── requirements.txt        # Dépendances (vide - libs standard)
├── .gitignore             # Configuration Git
├── README.md              # Ce fichier
└── LICENSE                # Licence MIT
```

## 🏗️ Architecture

Le projet suit le **pattern MVC (Model-View-Controller)** :

- **Models** (`models/`) : Définit la classe `Matiere` avec validation
- **Views** (`views/`) : Interface graphique Tkinter
- **Controller** (`controller.py`) : Gère la logique et les interactions
- **Utils** (`utils/`) : Fonctions utilitaires (calculs, validation)

## 🧪 Exemple

```python
from models.matiere import Matiere
from utils.calculs import calculer_moyenne

# Créer des matières
matieres = [
    Matiere("Mathématiques", 7, 16),
    Matiere("Français", 5, 14),
]

# Calculer la moyenne
moyenne = calculer_moyenne(matieres)
print(f"Moyenne: {moyenne:.2f}")  # Affiche: Moyenne: 15.27
```

## ⚙️ Coefficients par Défaut

| Matière | Coefficient |
|---------|------------|
| Mathématiques | 7 |
| Physique-Chimie | 6 |
| SVT | 6 |
| Français | 5 |
| Philosophie | 4 |
| Histoire-Géographie | 3 |
| Anglais | 3 |
| Espagnol | 2 |
| EPS | 2 |
| Spécialité 1 | 16 |
| Spécialité 2 | 16 |
| Grand Oral | 10 |

## 🐛 Signaler un Problème

Si vous trouvez un bug, veuillez ouvrir une [issue](https://github.com/votre-username/calculateur-moyenne/issues).

## 📝 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

Créé par **Sam** - 2026

## 🤝 Contribution

Les contributions sont bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request
