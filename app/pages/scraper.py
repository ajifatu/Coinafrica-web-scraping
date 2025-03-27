import streamlit as st
from scraper.bs_scraper import scrape_with_bs, CATEGORIES

def show():
    st.title("🔎 Scraper les données")

    st.markdown("Scraping dynamique avec **BeautifulSoup**")

    options = list(CATEGORIES.keys()) + ["Toutes les catégories"]
    selected_cat = st.selectbox("Choisir une catégorie", options)
    max_pages = st.slider("Nombre de pages à scraper", 1, 10, 1)

    if st.button("Lancer le scraping"):
        with st.spinner("Scraping en cours..."):
            if selected_cat == "Toutes les catégories":
                df = scrape_with_bs(max_pages=max_pages, all_categories=True)
            else:
                df = scrape_with_bs(category_url=CATEGORIES[selected_cat], max_pages=max_pages)

            st.success(f"{len(df)} annonces récupérées.")
            st.dataframe(df)

            st.download_button("📥 Télécharger CSV", df.to_csv(index=False).encode("utf-8"), file_name="donnees_scrapees.csv", mime="text/csv")
