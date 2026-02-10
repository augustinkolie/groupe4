# 🚀 Guide d'Installation EcoWatch

Ce guide vous permet d'installer et configurer le projet EcoWatch sur **n'importe quelle machine** et d'obtenir exactement le même environnement de travail.

---

## 📋 Prérequis système

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.8 ou supérieur** ([Télécharger Python](https://www.python.org/downloads/))
- **Git** ([Télécharger Git](https://git-scm.com/downloads))
- **Connexion Internet** (obligatoire pour les graphiques et les CDN)

### Vérifier les installations

```bash
# Vérifier Python
python --version
# Devrait afficher : Python 3.8.x ou supérieur

# Vérifier pip
pip --version

# Vérifier Git
git --version
```

---

## 📦 Étape 1 : Cloner le dépôt

```bash
# Cloner le projet
git clone <URL_DU_DEPOT>

# Accéder au dossier du projet
cd groupe4
```

---

## 🐍 Étape 2 : Créer l'environnement virtuel

### Sur Windows

```powershell
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
venv\Scripts\activate

# Votre terminal devrait maintenant afficher (venv) au début
```

### Sur Linux/Mac

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Votre terminal devrait maintenant afficher (venv) au début
```

---

## 📥 Étape 3 : Installer les dépendances Python

```bash
# S'assurer que l'environnement virtuel est activé (vous devez voir (venv))
# Installer toutes les dépendances
pip install -r requirements.txt
```

### Liste des dépendances installées

- Django 5.1.5 - Framework web
- djangorestframework - API REST
- django-cors-headers - Gestion CORS
- django-allauth - Authentification
- django-q2 - Tâches asynchrones
- matplotlib - **Graphiques backend**
- numpy - **Calculs numériques**
- reportlab - Génération PDF
- openpyxl - Export Excel
- requests - Appels HTTP
- python-dotenv - Variables d'environnement

---

## ⚙️ Étape 4 : Configuration de l'environnement

### Créer le fichier `.env`

Créez un fichier `.env` **à la racine du projet** avec le contenu suivant :

```env
# Configuration Django
SECRET_KEY=votre-cle-secrete-django-unique-et-longue
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données (SQLite par défaut)
DATABASE_URL=sqlite:///db.sqlite3

# API Keys (optionnel)
OPENWEATHER_API_KEY=votre_cle_api_si_disponible
```

> **⚠️ Important** : 
> - Ne **jamais** commiter le fichier `.env` dans Git (il doit être dans `.gitignore`)
> - Générez une nouvelle `SECRET_KEY` unique pour chaque environnement
> - En production, mettez `DEBUG=False`

### Générer une SECRET_KEY

```python
# Dans un terminal Python (après activation de venv)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiez la clé générée dans votre fichier `.env`.

---

## 🗄️ Étape 5 : Initialiser la base de données

```bash
# Appliquer les migrations
python manage.py migrate

# Créer un compte super-utilisateur (admin)
python manage.py createsuperuser
# Suivez les instructions pour créer votre compte admin
```

### Charger les données de démonstration (optionnel)

```bash
# Charger les stations de Guinée
python seed_guinea_stations.py

# Générer des données historiques
python generate_historical_data.py

# Créer des alertes de démonstration
python seed_demo_alerts.py
```

---

## 🎨 Étape 6 : Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

---

## 🚀 Étape 7 : Lancer le serveur

```bash
# Démarrer le serveur de développement
python manage.py runserver

# Le serveur démarre sur : http://127.0.0.1:8000
```

### Accéder à l'application

- **Frontend** : http://127.0.0.1:8000
- **Admin Django** : http://127.0.0.1:8000/admin
- **Dashboard** : http://127.0.0.1:8000/dashboard

---

## 🌐 Dépendances externes (CDN)

### Bibliothèques JavaScript chargées depuis Internet

L'application utilise les CDN suivants (connexion Internet **obligatoire**) :

| Bibliothèque | Usage | CDN |
|--------------|-------|-----|
| **Chart.js** | **Graphiques interactifs** | https://cdn.jsdelivr.net/npm/chart.js |
| Font Awesome | Icônes | https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css |
| Google Fonts (Inter) | Typographie | https://fonts.googleapis.com/css2 |
| HTMX | Interactions AJAX | https://unpkg.com/htmx.org@1.9.10 |

> **🔴 Critique** : Sans connexion Internet, les graphiques ne s'afficheront pas car Chart.js ne pourra pas être chargé.

---

## ✅ Checklist de vérification

Avant de dire que tout fonctionne, vérifiez :

- [ ] Python 3.8+ est installé
- [ ] Environnement virtuel créé et **activé** (vous voyez `(venv)`)
- [ ] `pip install -r requirements.txt` exécuté sans erreur
- [ ] Fichier `.env` créé avec une `SECRET_KEY` unique
- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Super-utilisateur créé
- [ ] Connexion Internet active
- [ ] Serveur démarré (`python manage.py runserver`)
- [ ] Page d'accueil accessible sur http://127.0.0.1:8000
- [ ] Graphiques visibles dans le dashboard

---

## 🐛 Résolution de problèmes courants

### Les graphiques ne s'affichent pas

**Cause** : Chart.js n'est pas chargé (pas de connexion Internet)

**Solution** :
1. Vérifiez votre connexion Internet
2. Ouvrez la console du navigateur (F12)
3. Cherchez les erreurs de chargement de scripts
4. Testez l'accès à : https://cdn.jsdelivr.net/npm/chart.js

**Vérification dans la console** :
```javascript
// Dans la console du navigateur (F12)
typeof Chart
// Doit retourner "function", sinon Chart.js n'est pas chargé
```

### Erreur "No module named..."

**Cause** : Dépendances Python non installées ou environnement virtuel non activé

**Solution** :
```bash
# Assurez-vous que (venv) apparaît dans votre terminal
# Si non, activez l'environnement :
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Réinstallez les dépendances
pip install -r requirements.txt
```

### Erreur "SECRET_KEY"

**Cause** : Fichier `.env` manquant ou mal configuré

**Solution** :
1. Créez le fichier `.env` à la racine
2. Ajoutez `SECRET_KEY=...` avec une clé générée

### La base de données est vide

**Solution** :
```bash
# Chargez les données de démonstration
python seed_guinea_stations.py
python generate_historical_data.py
python seed_demo_alerts.py
```

### Port 8000 déjà utilisé

**Solution** :
```bash
# Utilisez un autre port
python manage.py runserver 8080

# Accédez à : http://127.0.0.1:8080
```

---

## 🔄 Arrêter et redémarrer

### Arrêter le serveur

- Appuyez sur `Ctrl + C` dans le terminal

### Désactiver l'environnement virtuel

```bash
deactivate
```

### Redémarrer (sessions futures)

```bash
# 1. Aller dans le dossier du projet
cd groupe4

# 2. Activer l'environnement virtuel
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Lancer le serveur
python manage.py runserver
```

---

## 📂 Structure du projet

```
groupe4/
├── venv/                     # Environnement virtuel (ne pas commiter)
├── monitoring/               # Application principale
│   ├── templates/           # Templates HTML
│   ├── static/              # Fichiers CSS/JS
│   └── views.py            # Vues Django
├── ecowatch/                # Configuration Django
│   └── settings.py         # Paramètres du projet
├── media/                   # Fichiers uploadés
├── templates/               # Templates de base
├── db.sqlite3              # Base de données (ne pas commiter en prod)
├── .env                    # Variables d'environnement (ne pas commiter)
├── .gitignore              # Fichiers à ignorer par Git
├── requirements.txt        # Dépendances Python
├── manage.py               # Script de gestion Django
└── INSTALLATION.md         # Ce fichier
```

---

## 🔐 Sécurité - Important pour le déploiement

### Fichiers à NE JAMAIS commiter dans Git

- `.env` - Contient les secrets
- `db.sqlite3` - Base de données locale
- `venv/` - Environnement virtuel
- `__pycache__/` - Cache Python
- `*.pyc` - Fichiers Python compilés

### Vérifiez votre `.gitignore`

```gitignore
# Environnement
.env
venv/
venv_groupe4/

# Base de données
*.sqlite3
db.sqlite3

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Django
*.log
staticfiles/
media/

# IDE
.vscode/
.idea/
*.swp
*.swo
```

---

## 🌍 Déploiement en production

Pour déployer en production (Heroku, AWS, etc.) :

1. **Changez `DEBUG=False`** dans `.env`
2. **Configurez `ALLOWED_HOSTS`** avec votre domaine
3. **Utilisez PostgreSQL** au lieu de SQLite
4. **Configurez les fichiers statiques** avec WhiteNoise ou S3
5. **Utilisez Gunicorn** comme serveur WSGI
6. **Ajoutez HTTPS** avec Let's Encrypt

---

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez les logs du serveur dans le terminal
2. Ouvrez la console du navigateur (F12 → Console)
3. Vérifiez que toutes les étapes ont été suivies
4. Consultez la documentation Django : https://docs.djangoproject.com/

---

**Version** : 1.0  
**Dernière mise à jour** : Février 2026  
**Projet** : EcoWatch - Plateforme de surveillance de la qualité de l'air
