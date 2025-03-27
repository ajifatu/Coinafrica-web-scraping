import streamlit as st
from scraper.bs_scraper import scrape_with_bs, CATEGORIES as CAT_BS
from scraper.selenium_scraper import scrape_with_selenium, CATEGORIES as CAT_SELENIUM

def show():
    st.title("🔎 Scraper les données")

    st.markdown("Scraping dynamique : choisissez votre méthode")

    # Scraper au choix
    scraper_choice = st.radio("Choisissez l’outil de scraping", ["BeautifulSoup", "Selenium"])

    # Catégories
    categories = list(CAT_BS.keys()) + ["Toutes les catégories"]
    selected_cat = st.selectbox("Choisir une catégorie", categories)

    # Nombre de pages
    max_pages = st.slider("Nombre de pages à scraper", 1, 10, 1)

    if st.button("Lancer le scraping"):
        with st.spinner("Scraping en cours..."):

            all_categories = selected_cat == "Toutes les catégories"
            category_url = CAT_BS.get(selected_cat)  # same keys for both dicts

            if scraper_choice == "BeautifulSoup":
                df = scrape_with_bs(
                    category_url=category_url,
                    max_pages=max_pages,
                    all_categories=all_categories
                )
            else:
                df = scrape_with_selenium(
                    category_url=category_url,
                    max_pages=max_pages,
                    all_categories=all_categories
                )

            st.success(f"{len(df)} annonces récupérées.")
            st.dataframe(df)

            st.download_button(
                "📥 Télécharger CSV",
                df.to_csv(index=False).encode("utf-8"),
                file_name="donnees_scrapees.csv",
                mime="text/csv"
            )
