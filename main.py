import streamlit as st
import pandas as pd

raw_data_webscraper =pd.read_csv("data/coinafrique_rawData_webScraper.csv")
st.write(raw_data_webscraper)