import streamlit as st
import pandas as pd
import os

def show():
    st.title("Données brutes (Web Scraper)")

    data_path = "data/raw/coinafrique_rawData_webScraper.csv"

    if not os.path.exists(data_path):
        st.warning("Aucun fichier Web Scraper trouvé dans data/raw.")
        return

    # Chargement des données
    df = pd.read_csv(data_path)

    st.success(f"{len(df)} lignes chargées.")

    # --- Filtres dynamiques ---
    col1, col2, col3 = st.columns(3)

    with col1:
        categories = df["categorie"].dropna().unique()
        selected_cats = st.multiselect("Filtrer par catégorie", categories, default=categories)

    with col2:
        anciennetes = df["anciennete"].dropna().unique()
        selected_anciennete = st.multiselect("Filtrer par ancienneté", anciennetes, default=anciennetes)

    with col3:
        if "Propriétaire" in df.columns:
            proprios = df["proprio"].dropna().unique()
            selected_proprio = st.multiselect("Filtrer par proprio", proprios)
        else:
            selected_proprio = []

    # Application des filtres
    filtered_df = df.copy()

    if selected_cats:
        filtered_df = filtered_df[filtered_df["categorie"].isin(selected_cats)]

    if selected_anciennete:
        filtered_df = filtered_df[filtered_df["anciennete"].isin(selected_anciennete)]

    if selected_proprio:
        filtered_df = filtered_df[filtered_df["proprio"].isin(selected_proprio)]


    # --- Affichage ---
    st.dataframe(filtered_df)

    # --- Téléchargement ---
    st.download_button(
        " Télécharger les données filtrées (CSV)",
        filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="donnees_webscraper_filtrees.csv",
        mime="text/csv"
    )
