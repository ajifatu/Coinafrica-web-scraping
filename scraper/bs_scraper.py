import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

CATEGORIES = {
    "Chiens": "https://sn.coinafrique.com/categorie/chiens",
    "Moutons": "https://sn.coinafrique.com/categorie/moutons",
    "Poules, lapins et pigeons": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
    "Autres animaux": "https://sn.coinafrique.com/categorie/autres-animaux"
}

def scrape_with_bs(category_url=None, max_pages=1, all_categories=False):
    base_url = "https://sn.coinafrique.com"
    data = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    target_categories = CATEGORIES.items() if all_categories else [("Unique", category_url)]

    for cat_name, url in target_categories:
        for page in range(1, max_pages + 1):
            full_url = f"{url}?page={page}"
            res = requests.get(full_url, headers=headers)
            soup = BeautifulSoup(res.text, "lxml")

            cards = soup.select("div[class^='AdCard_AdCard']")

            for card in cards:
                nom = card.select_one("h2").text.strip() if card.select_one("h2") else ""
                prix = card.select_one("div[class*='PriceDisplay']").text.strip() if card.select_one("div[class*='PriceDisplay']") else ""
                adresse = card.select_one("div[class*='AdCard_location']").text.strip() if card.select_one("div[class*='AdCard_location']") else ""
                image_tag = card.select_one("img")
                image_lien = image_tag["src"] if image_tag and image_tag.has_attr("src") else ""

                proprio = card.select_one("span[class*='AdCard_ownerName']")
                proprio = proprio.text.strip() if proprio else ""

                anciennete = card.select_one("div[class*='AdCard_footer']")
                anciennete = anciennete.text.strip() if anciennete else ""

                data.append({
                    "Catégorie": cat_name,
                    "Nom": nom,
                    "Prix": prix,
                    "Adresse": adresse,
                    "Propriétaire": proprio,
                    "Ancienneté": anciennete,
                    "Image": image_lien
                })

            time.sleep(1)  # anti-bot

    return pd.DataFrame(data)
