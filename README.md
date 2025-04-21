
# Tunisie Annonce Scraper API

Ce projet est une **API REST avec FastAPI** qui permet de lancer un **scraping d'annonces immobilières** depuis le site [tunisie-annonce.com](http://www.tunisie-annonce.com), et de consulter les données collectées via des endpoints.

---

##  Arborescence du projet

```
projet-scraping-api/
│
├── scraping/
│   └── scraper.py           # Script principal de scraping avec Selenium
│
├── api/
│   └── main.py              # API FastAPI avec les endpoints
│
├── data/
│   └── annonces.json        # (généré) Fichier JSON contenant les résultats du scraping
│
├── chromedriver/           
│   └── chromedriver.exe     # WebDriver pour Google Chrome
│
├── venv/                    # Environnement virtuel Python
│
└── requirements.txt         # Liste des dépendances
```

---

##  Prérequis

- Python 3.10 ou +
- Google Chrome installé
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) (déjà inclus ici)
- Accès Internet

---

## 🔧 Installation

1. **Cloner le projet** :

```bash
git clone https://github.com/Maram-r/scraping-annonces-tunisie.git
cd projet-scraping-api
```

2. **Activer l’environnement virtuel** :

Sous Windows :
```bash
venv\Scripts\activate
```

Sous Mac/Linux :
```bash
source venv/bin/activate
```

3. **Installer les dépendances** :

```bash
pip install -r requirements.txt
```

> Si tu n’as pas encore de `requirements.txt`, crée-le avec :
```bash
pip freeze > requirements.txt
```

Exemple de contenu :
```
fastapi
uvicorn
selenium
beautifulsoup4
```

---

## 🚀 Lancer l’API

Assure-toi d’être dans l’environnement virtuel, puis lance :

```bash
uvicorn api.main:app --reload
```

Tu devrais voir :

```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

##  Endpoints de l’API

###  `POST /scrape`

Lance une session de scraping.

- **Paramètre (query)** : `n_pages` (int, optionnel) → Nombre de pages à scraper (par défaut : 1)

Exemple avec `curl` :
```bash
curl -X POST "http://127.0.0.1:8000/scrape?n_pages=2"
```

###  `GET /annonces`

Retourne toutes les annonces collectées dans `data/annonces.json`.

Exemple :
```bash
curl http://127.0.0.1:8000/annonces
```

---

##  Tester dans Swagger UI

Va sur :
```
http://127.0.0.1:8000/docs
```

Tu peux interagir facilement avec tous les endpoints via une interface graphique générée automatiquement.

---

## 🛠️ Développement et structure

- `scraping/scraper.py` : contient la fonction `scraper_annonces(n_pages)` qui utilise Selenium pour naviguer sur le site.
- `api/main.py` : expose l’API via FastAPI.
- `data/annonces.json` : contient les résultats du scraping sous forme de liste d'objets JSON.

---

##  Exemple de résultat JSON

```json
[
  {
    "titre": "Appartement s2 à vendre",
    "type": "Appartement",
    "nature": "Vente",
    "rubrique": "Immobilier",
    "gouvernorat": "Tunis",
    "delegation": "La Marsa",
    "localite": "Gammarth",
    "description": "Appartement s2 hst à boumhal",
    "prix": "250 000 TND",
    "date_publication": "2025-01-15",
    "lien": "http://www.tunisie-annonce.com/..."
  }
]
```

---

##  Remarques

- Le scraping utilise Selenium → il ouvre une vraie fenêtre Chrome.
- Tu peux réduire le `time.sleep` dans le script si le chargement est rapide.
