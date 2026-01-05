# Calculateur de Moyenne - Trois Versions 🎯

Une application pour calculer les moyennes scolaires, disponible en **3 versions** :

1. **Desktop (Tkinter)** - Version classique pour Windows/Mac/Linux
2. **Web (Flask)** - Version accessible depuis n'importe quel navigateur
3. **Mobile (Kivy)** - Version pour Android/iOS

---

## 🚀 Installation Rapide

### Version Desktop (Tkinter)
```bash
git clone https://github.com/goldensam777/Calculateur-de-Moyennes.git
cd Calculateur-de-Moyennes
python main.py
```

### Version Web (Flask)
```bash
pip install -r requirements.txt
python web_app.py
# Puis ouvrez http://localhost:5000
```

### Version Mobile (Kivy)
```bash
pip install -r requirements.txt
python kivy_app.py
```

---

## 📊 Comparaison des Versions

| Caractéristique | Tkinter | Flask | Kivy |
|-----------------|---------|-------|------|
| **Plateforme** | Desktop | Web | Mobile |
| **Installation** | Simple | Simple | Moyen |
| **Performance** | Excellente | Très bonne | Bonne |
| **Design** | Basique | Moderne | Material |
| **Accès** | Local | Réseau | Local |
| **Sauvegarde** | Non | Facile | Facile |
| **Responsive** | Non | Oui | Oui |

---

## 💻 Version Desktop (Tkinter)

### Utilisation
1. Lancez `python main.py`
2. Saisissez vos notes (0-20)
3. Cochez les matières à inclure
4. Cliquez "Calculer la moyenne"

### Fonctionnalités
- ✅ Calcul pondéré
- ✅ Ajouter/supprimer des matières
- ✅ Validation en temps réel
- ✅ Appréciation avec couleurs

### Avantages
- Très rapide
- Aucune dépendance
- Simple et intuitif

---

## 🌐 Version Web (Flask)

### Utilisation
```bash
python web_app.py
# Accédez à http://localhost:5000
```

### Fonctionnalités
- ✅ Interface moderne et responsiv
- ✅ Fonctionne sur tous les navigateurs
- ✅ Accessible depuis le réseau local
- ✅ Ajouter/supprimer des matières dynamiquement
- ✅ Pas de rechargement de page

### Avantages
- Beau design (gradient, animations)
- Accessibilité mobile
- Facile à déployer (Heroku, AWS, etc.)

### Déployer en ligne
```bash
# Avec Heroku
git push heroku main

# Avec PythonAnywhere
# Copier les fichiers et configurer l'app web
```

---

## 📱 Version Mobile (Kivy)

### Installation
```bash
pip install kivy
python kivy_app.py
```

### Compilation APK pour Android
```bash
# Installer buildozer
pip install buildozer cython

# Compiler en APK
buildozer android debug

# Le fichier APK sera dans ./bin/
```

### Compilation IPA pour iOS
```bash
# Nécessite macOS
pip install kivy kivy-ios

# Compiler
toolchain create Calculateur python=3.9
# ... (processus complexe, consulter la doc Kivy)
```

### Fonctionnalités
- ✅ Interface tactile optimisée
- ✅ Ajouter/supprimer des matières
- ✅ Résultats en temps réel
- ✅ Sauvegarde locale

### Avantages
- Interface tactile native
- Fonctionnalités mobiles
- Distributio via App Store

---

## 🏗️ Architecture Partagée

Les trois versions utilisent la **même logique de calcul** dans `calculs.py` :

```python
# Partagé par toutes les versions
from calculs import Matiere, calculer_moyenne, obtenir_appreciation
```

Cela permet de :
- Garantir la cohérence
- Faciliter les mises à jour
- Partager les tests unitaires

---

## 📦 Prérequis

### Pour Tkinter
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS
brew install python-tk
```

### Pour Flask
```bash
pip install Flask==2.3.0
```

### Pour Kivy
```bash
pip install Kivy==2.2.0
```

---

## 🧪 Tester les Trois Versions

```bash
# Terminal 1 : Tkinter
python main.py

# Terminal 2 : Flask (après Terminal 1)
python web_app.py
# http://localhost:5000

# Terminal 3 : Kivy
python kivy_app.py
```

---

## 🚀 Prochaines Étapes

### Pour améliorer les trois versions :

1. **Sauvegarde de profils**
   - Tkinter : JSON local
   - Flask : Cookies ou base de données
   - Kivy : SharedPreferences (Android)

2. **Export PDF**
   - Tkinter : reportlab
   - Flask : html2pdf
   - Kivy : reportlab

3. **Synchronisation cloud**
   - Firebase pour toutes les versions

4. **Thème sombre**
   - CSS pour Flask
   - Kivy theme builder

---

## 📝 Licence

MIT License - Libre d'utilisation

---

## 💡 Consells Personnalisés

**Je utilise Tkinter si :**
- Tu veux quelque chose de simple et rapide
- Tu cibles seulement desktop

**Je utilise Flask si :**
- Tu veux un beau design moderne
- Tu veux l'accessibilité web/mobile
- Tu veux déployer en ligne

**Je utilise Kivy si :**
- Tu veux une app native mobile
- Tu veux distribuer sur App Store
- Tu as besoin de features mobiles (GPS, etc.)

---

## 📞 Support

Pour des questions ou problèmes :
- GitHub Issues: https://github.com/goldensam777/Calculateur-de-Moyennes/issues
- Email: sam@example.com

---

**Bon calcul ! 📊**
