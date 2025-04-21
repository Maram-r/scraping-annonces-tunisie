""" from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import json
import os

def extraire_info_depuis_onmouseover(attribut):
   Extrait un dictionnaire depuis le contenu HTML dans onmouseover.
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(attribut, "html.parser")
    return {b.get_text(strip=True).rstrip(':'): b.next_sibling.strip() for b in soup.find_all('b')}

def load_annonces():
    try:
        with open('data/annonces.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def scrape_data():
    print("Début du scraping...")

    # Lancer le navigateur
    service = Service("C:/projet-scraping-api/chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("http://www.tunisie-annonce.com/AnnoncesImmobilier.asp")
    
    time.sleep(10)  # attendre le chargement

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    annonces = soup.find_all('tr', class_='Tableau1')
    base_url = "https://www.tunisie-annonce.com/"

    annonces_list = []

    for ann in annonces:
        try:
            tds = ann.find_all('td')
            if len(tds) >= 12:
                # Localisation complète (ville, délégation...)
                loc_mouse = tds[1].find('a')['onmouseover']
                localisation_info = extraire_info_depuis_onmouseover(loc_mouse)

                # Type et nature du bien
                type_mouse = tds[3]['onmouseover']
                type_info = extraire_info_depuis_onmouseover(type_mouse)

                # Titre + description
                titre_tag = tds[7].find('a')
                desc_mouse = titre_tag['onmouseover']
                description_info = extraire_info_depuis_onmouseover(desc_mouse)

                # Lien complet
                lien = base_url + titre_tag['href'] if titre_tag else None

                # Prix
                prix = tds[9].get_text(strip=True)

                # Date publication
                date_pub = tds[11].get_text(strip=True)

                annonce = {
                    "titre": titre_tag.get_text(strip=True),
                    "type": type_info.get("Type"),
                    "nature": type_info.get("Nature"),
                    "rubrique": type_info.get("Rubrique"),
                    "gouvernorat": localisation_info.get("Gouvernorat"),
                    "delegation": localisation_info.get("Délégation"),
                    "localite": localisation_info.get("Localité"),
                    "description": description_info.get("Appartement s2 hst à boumhal", ""),  # fallback
                    "prix": prix,
                    "date_publication": date_pub,
                    "lien": lien
                }

                annonces_list.append(annonce)

        except Exception as e:
            print("Erreur lors du traitement d'une annonce :", e)

    os.makedirs("data", exist_ok=True)
    with open('data/annonces.json', 'w', encoding='utf-8') as json_file:
        json.dump(annonces_list, json_file, indent=4, ensure_ascii=False)

    driver.quit()
    print(f"{len(annonces_list)} annonces extraites. Scraping terminé.")
 """
"""import time
import json
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Fonction robuste pour extraire les champs à partir du onmouseover
def extraire_info_depuis_onmouseover(info_str):
    info_dict = {}
    try:
        gouvernorat = re.search(r"<b>Gouvernorat</b> : (.*?)<br/>", info_str)
        delegation = re.search(r"<b>Délégation</b> : (.*?)<br/>", info_str)
        localite = re.search(r"<b>Localité</b> : (.*?)<br/>", info_str)
        type_ = re.search(r"<b>Type</b> : (.*?)<br/>", info_str)
        nature = re.search(r"<b>Nature</b> : (.*?)<br/>", info_str)
        rubrique = re.search(r"<b>Rubrique</b> : (.*?)<br/>", info_str)
        description = re.search(r"<b>Description</b> : (.*?)<br/>", info_str)

        if gouvernorat: info_dict["Gouvernorat"] = gouvernorat.group(1)
        if delegation: info_dict["Délégation"] = delegation.group(1)
        if localite: info_dict["Localité"] = localite.group(1)
        if type_: info_dict["Type"] = type_.group(1)
        if nature: info_dict["Nature"] = nature.group(1)
        if rubrique: info_dict["Rubrique"] = rubrique.group(1)
        if description: info_dict["Description"] = description.group(1)

    except Exception as e:
        print("Erreur dans l'extraction :", e)

    return info_dict

# Initialiser Selenium
print("Début du scraping...")
service = Service("C:/projet-scraping-api/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("http://www.tunisie-annonce.com/AnnoncesImmobilier.asp")

time.sleep(10)  # Attendre le chargement

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
annonces = soup.find_all('tr', class_='Tableau1')

base_url = "https://www.tunisie-annonce.com/"
annonces_list = []

for ann in annonces:
    try:
        tds = ann.find_all('td')
        if len(tds) >= 12:
            # Localisation
            loc_mouse = tds[1].find('a')['onmouseover']
            localisation_info = extraire_info_depuis_onmouseover(loc_mouse)

            # Type/nature/rubrique
            type_mouse = tds[3].get('onmouseover', '')
            type_info = extraire_info_depuis_onmouseover(type_mouse)

            # Titre & description
            titre_tag = tds[7].find('a')
            lien = base_url + titre_tag['href'] if titre_tag else None
            desc_mouse = titre_tag.get('onmouseover', '')
            desc_info = extraire_info_depuis_onmouseover(desc_mouse)

            # Prix & date
            prix = tds[9].get_text(strip=True)
            date_pub = tds[11].get_text(strip=True)

            # Création de l'annonce
            annonce = {
                "titre": titre_tag.get_text(strip=True) if titre_tag else "Titre non disponible",
                "type": type_info.get("Type"),
                "nature": type_info.get("Nature"),
                "rubrique": type_info.get("Rubrique"),
                "gouvernorat": localisation_info.get("Gouvernorat"),
                "delegation": localisation_info.get("Délégation"),
                "localite": localisation_info.get("Localité"),
                "description": desc_info.get("Description"),
                "prix": prix,
                "date_publication": date_pub,
                "lien": lien
            }

            annonces_list.append(annonce)

    except Exception as e:
        print("Erreur dans une annonce :", e)

# Sauvegarde
os.makedirs("data", exist_ok=True)
with open('data/annonces.json', 'w', encoding='utf-8') as f:
    json.dump(annonces_list, f, indent=4, ensure_ascii=False)

print("Scraping terminé et données enregistrées dans 'data/annonces.json'.")  
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def extraire_info_depuis_onmouseover(info_str):
    info_dict = {}
    try:
        if '<b>Gouvernorat</b> : ' in info_str:
            info_dict['Gouvernorat'] = info_str.split('<b>Gouvernorat</b> : ')[1].split('<br/>')[0]
        if '<b>Délégation</b> : ' in info_str:
            info_dict['Délégation'] = info_str.split('<b>Délégation</b> : ')[1].split('<br/>')[0]
        if '<b>Localité</b> : ' in info_str:
            info_dict['Localité'] = info_str.split('<b>Localité</b> : ')[1].split('<br/>')[0]
        if '<b>Type</b> : ' in info_str:
            info_dict['Type'] = info_str.split('<b>Type</b> : ')[1].split('<br/>')[0]
        if '<b>Nature</b> : ' in info_str:
            info_dict['Nature'] = info_str.split('<b>Nature</b> : ')[1].split('<br/>')[0]
        if '<b>Rubrique</b> : ' in info_str:
            info_dict['Rubrique'] = info_str.split('<b>Rubrique</b> : ')[1].split('<br/>')[0]
        if '<b>Description</b> : ' in info_str:
            info_dict['Description'] = info_str.split('<b>Description</b> : ')[1].split('<br/>')[0]
    except Exception as e:
        print("Erreur dans l'extraction des infos:", e)
    return info_dict


def scraper_annonces(n_pages: int = 1) -> list:
    service = Service("C:/projet-scraping-api/chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    base_url = "http://www.tunisie-annonce.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_order_by=31&rech_page_num="
    base_lien = "http://www.tunisie-annonce.com/"
    
    annonces_list = []

    for page in range(1, n_pages + 1):
        print(f"Scraping page {page}...")
        driver.get(base_url + str(page))
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        annonces = soup.find_all('tr', class_='Tableau1')

        for ann in annonces:
            try:
                tds = ann.find_all('td')
                if len(tds) >= 12:
                    # Localisation
                    loc_mouse = tds[1].find('a')['onmouseover']
                    localisation_info = extraire_info_depuis_onmouseover(loc_mouse)

                    # Type/nature
                    type_mouse = tds[3].get('onmouseover', '')
                    type_info = extraire_info_depuis_onmouseover(type_mouse)

                    # Titre et description
                    titre_tag = tds[7].find('a')
                    desc_mouse = titre_tag.get('onmouseover', '') if titre_tag else ''
                    description_info = extraire_info_depuis_onmouseover(desc_mouse)

                    lien = base_lien + titre_tag['href'] if titre_tag else None
                    prix = tds[9].get_text(strip=True)
                    date_pub = tds[11].get_text(strip=True)

                    annonce = {
                        "titre": titre_tag.get_text(strip=True) if titre_tag else "Titre non disponible",
                        "type": type_info.get("Type", "Non spécifié"),
                        "nature": type_info.get("Nature", "Non spécifié"),
                        "rubrique": type_info.get("Rubrique", "Non spécifié"),
                        "gouvernorat": localisation_info.get("Gouvernorat", "Non spécifié"),
                        "delegation": localisation_info.get("Délégation", "Non spécifié"),
                        "localite": localisation_info.get("Localité", "Non spécifié"),
                        "description": description_info.get("Description", "Non spécifié"),
                        "prix": prix,
                        "date_publication": date_pub,
                        "lien": lien
                    }

                    annonces_list.append(annonce)
            except Exception as e:
                print("Erreur lors du traitement d'une annonce :", e)

    driver.quit()
    return annonces_list

