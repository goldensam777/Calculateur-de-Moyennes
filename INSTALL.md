# Installation du Calculateur de Moyenne

## 📦 Option 1 : Installation via pip (Recommended)

### Depuis GitHub
```bash
pip install git+https://github.com/goldensam777/Calculateur-de-Moyennes.git
```

### Puis lancer l'application
```bash
calculateur-moyenne
```

---

## 🔧 Option 2 : Installation locale en mode développement

### Cloner le dépôt
```bash
git clone https://github.com/goldensam777/Calculateur-de-Moyennes.git
cd Calculateur-de-Moyennes
```

### Créer un environnement virtuel (recommandé)
```bash
python -m venv venv

# Sur Linux/Mac :
source venv/bin/activate

# Sur Windows :
venv\Scripts\activate
```

### Installer en mode développement
```bash
pip install -e .
```

### Lancer l'application
```bash
calculateur-moyenne
# ou
python main.py
```

---

## 🐳 Option 3 : Utilisation directe (sans installation)

### Exécuter directement
```bash
git clone https://github.com/goldensam777/Calculateur-de-Moyennes.git
cd Calculateur-de-Moyennes
python main.py
```

---

## ✅ Prérequis

- **Python 3.6+**
- **Tkinter** (généralement inclus avec Python)

### Vérifier l'installation de Tkinter
```bash
python -m tkinter
```

Si une fenêtre vide apparaît, Tkinter est installé correctement.

### Installer Tkinter si manquant

**Sur Ubuntu/Debian :**
```bash
sudo apt-get install python3-tk
```

**Sur Fedora :**
```bash
sudo dnf install python3-tkinter
```

**Sur macOS :**
```bash
brew install python-tk
```

**Sur Windows :**
Tkinter est inclus avec Python. Assurez-vous de cocher "tcl/tk and IDLE" lors de l'installation.

---

## 🚀 Utilisation

1. Lancez l'application
2. Saisissez vos notes (0-20) pour chaque matière
3. Cochez les matières à inclure dans le calcul
4. Cliquez sur "**Calculer la moyenne**"
5. Consultez le résultat avec l'interprétation

---

## 🆘 Dépannage

### Erreur : "No module named 'tkinter'"
→ Installez Tkinter (voir ci-dessus)

### Erreur : "No module named 'main'"
→ Assurez-vous que vous êtes dans le bon répertoire

### L'application se lance mais est vide
→ Attendez quelques secondes pour que l'interface se charge

---

## 📝 Licence

MIT License - voir le fichier LICENSE
