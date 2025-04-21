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

