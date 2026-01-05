# 🚀 Déployer sur Vercel

## Pourquoi Vercel ?

✅ **Gratuit** - Jusqu'à 100 déploiements par mois
✅ **Rapide** - Déploiement en 30 secondes
✅ **Scalable** - Serverless functions
✅ **SSL Gratuit** - Certificat HTTPS inclus
✅ **Domaine personnalisé** - Gratuit aussi

---

## 📋 Prérequis

1. Un compte GitHub (vous l'avez déjà ✅)
2. Un compte Vercel (gratuit)
3. Le CLI Vercel (optionnel)

---

## 🎯 Déploiement en 5 Minutes

### Option 1 : Via Vercel Dashboard (Plus facile)

1. **Allez sur** https://vercel.com/signup
2. **Cliquez** "Continue with GitHub"
3. **Autorisez** Vercel à accéder à vos repos
4. **Cliquez** "Import Project"
5. **Sélectionnez** `Calculateur-de-Moyennes`
6. **Vercel détectera** automatiquement Flask
7. **Cliquez** "Deploy"

**C'est fait ! 🎉**

Votre app sera à : `https://calculateur-de-moyennes.vercel.app`

---

### Option 2 : Via CLI (Pour les pros)

```bash
# Installer Vercel CLI
npm i -g vercel

# Depuis le dossier du projet
cd Calculateur-de-Moyennes

# Se connecter
vercel login

# Déployer
vercel

# Répondre aux questions (accepter les defaults)
```

---

## ⚙️ Configuration (Déjà faite ✅)

Le fichier `vercel.json` contient tout ce qu'il faut :

```json
{
  "version": 2,
  "builds": [
    {
      "src": "web_app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "web_app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

---

## 🗄️ Gestion de la Base de Données

### ⚠️ Important : Vercel + SQLite

Vercel utilise un **système de fichiers éphémère** = les fichiers .db **disparaissent après 24h**.

### Solutions :

#### ✅ Solution 1 : PostgreSQL (Recommandé)
```bash
# 1. Créer une base PostgreSQL gratuite sur Railway.app
# 2. Copier l'URL de connexion
# 3. Remplacer SQLite par psycopg2
```

#### ✅ Solution 2 : MongoDB Atlas (Gratuit)
```bash
# Simpler à mettre en place, gratuit aussi
pip install pymongo
```

#### ✅ Solution 3 : Supabase (Meilleur rapport)
```bash
# PostgreSQL gratuit + interface web + auth
# https://supabase.io
```

**Quelle solution tu veux ?**

---

## 🔗 Domaine Personnalisé

Une fois déployé sur Vercel :

1. Allez sur https://vercel.com/dashboard
2. Sélectionnez votre projet
3. Allez à "Settings" → "Domains"
4. Entrez votre domaine : `moyenne.tonnom.com`
5. Suivez les instructions DNS

**Coûts :**
- Vercel : GRATUIT
- Domaine (.com) : ~10€/an chez Namecheap

---

## 🔄 Déploiement Automatique

À chaque `git push` :

1. GitHub notifie Vercel
2. Vercel récupère le code
3. Vercel build et déploie
4. **30 secondes plus tard = en ligne** ✅

Aucune action manuelle !

```bash
# Juste faire ça normalement
git add .
git commit -m "update: ..."
git push origin main
```

---

## 📊 Monitoring

Sur le dashboard Vercel, vous pouvez voir :

- ✅ **Derniers déploiements**
- 📊 **Statistiques d'utilisation**
- 🔴 **Erreurs et logs**
- ⚡ **Performance**

---

## 🐛 Troubleshooting

### "Build failed"
```
→ Vérifie requirements.txt
→ Vérifie que web_app.py est à la racine
→ Regarde les logs sur Vercel
```

### "Application Error"
```
→ Les logs Vercel expliquent l'erreur
→ Généralement : import manquant ou typo
```

### "Database connection failed"
```
→ Normal avec SQLite sur Vercel
→ Utilise PostgreSQL/MongoDB à la place
```

---

## 💰 Coûts

| Service | Gratuit | Prix |
|---------|---------|------|
| Vercel | ✅ Oui | - |
| Domaine | ❌ Non | ~10€/an |
| PostgreSQL (Railway) | ✅ $5/mois | +$0.20/GB |
| MongoDB Atlas | ✅ Oui | - |

**Total minimum : Gratuit (avec MongoDB)**
**Total pro : ~10€/an (avec domaine)**

---

## 📱 Tester en Local avant Deployer

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer en mode prod
export FLASK_ENV=production
python web_app.py

# Tester
curl http://localhost:5000
```

---

## 🎯 Prochaines Étapes

1. **Choisir la solution DB** (PostgreSQL/MongoDB)
2. **Créer un compte Vercel**
3. **Importer le projet**
4. **Configurer les variables d'environnement**
5. **Déployer ! 🚀**

---

## 📞 Support Vercel

- **Docs** : https://vercel.com/docs
- **Status** : https://www.vercelstatus.com
- **Help** : https://vercel.com/support

---

**Besoin d'aide ? Je peux t'aider avec PostgreSQL ou MongoDB ! 💪**
