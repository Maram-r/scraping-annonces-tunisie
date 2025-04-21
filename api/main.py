from fastapi import FastAPI
from scraping.scraper import scraper_annonces
import json
import os

app = FastAPI()

DATA_FILE = "data/annonces.json"

# GET /annonces → retourne les annonces stockées
@app.get("/annonces")
def get_annonces():
    if not os.path.exists(DATA_FILE):
        return {"message": "Aucune annonce trouvée"}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        annonces = json.load(f)
    return {"nb_annonces": len(annonces), "annonces": annonces}

# POST /scrape → lance une nouvelle session de scraping
@app.post("/scrape")
def lancer_scraping(n_pages: int = 1):
    annonces = scraper_annonces(n_pages)
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(annonces, f, indent=4, ensure_ascii=False)
    return {"message": f"{len(annonces)} annonces extraites et sauvegardées avec succès."}
