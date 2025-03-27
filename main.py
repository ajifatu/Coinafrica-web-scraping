import streamlit as st
from app.pages import show_raw_data, show_scraper, show_dashboard, show_evaluation

st.set_page_config(page_title="CoinAfrique Animal Scraper", layout="wide")
st.sidebar.title("Menu")

page = st.sidebar.radio("Navigation", [
    "Données brutes (Web Scraper)",
    "Scraper les données",
    "Dashboard",
    "Évaluation"
])

if page == "Données brutes (Web Scraper)":
    show_raw_data()

elif page == "Scraper les données":
    show_scraper()

elif page == "Dashboard":
    show_dashboard()

elif page == "Évaluation":
    show_evaluation()
