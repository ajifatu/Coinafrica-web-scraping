from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

CATEGORIES = {
    "Chiens": "https://sn.coinafrique.com/categorie/chiens",
    "Moutons": "https://sn.coinafrique.com/categorie/moutons",
    "Poules, lapins et pigeons": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
    "Autres animaux": "https://sn.coinafrique.com/categorie/autres-animaux"
}

def scrape_with_selenium(category_url=None, max_pages=1, all_categories=False):
    data = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)

    target_categories = CATEGORIES.items() if all_categories else [("Unique", category_url)]

    for cat_name, url in target_categories:
        for page in range(1, max_pages + 1):
            full_url = f"{url}?page={page}"
            driver.get(full_url)
            time.sleep(2)

            cards = driver.find_elements(By.CSS_SELECTOR, "div[class^='AdCard_AdCard']")

            for card in cards:
                try:
                    nom = card.find_element(By.TAG_NAME, "h2").text
                except: nom = ""

                try:
                    prix = card.find_element(By.CSS_SELECTOR, "div[class*='PriceDisplay']").text
                except: prix = ""

                try:
                    adresse = card.find_element(By.CSS_SELECTOR, "div[class*='AdCard_location']").text
                except: adresse = ""

                try:
                    image_lien = card.find_element(By.TAG_NAME, "img").get_attribute("src")
                except: image_lien = ""

                try:
                    proprio = card.find_element(By.CSS_SELECTOR, "span[class*='AdCard_ownerName']").text
                except: proprio = ""

                try:
                    anciennete = card.find_element(By.CSS_SELECTOR, "div[class*='AdCard_footer']").text
                except: anciennete = ""

                data.append({
                    "Catégorie": cat_name,
                    "Nom": nom,
                    "Prix": prix,
                    "Adresse": adresse,
                    "Propriétaire": proprio,
                    "Ancienneté": anciennete,
                    "Image": image_lien
                })

    driver.quit()
    return pd.DataFrame(data)
