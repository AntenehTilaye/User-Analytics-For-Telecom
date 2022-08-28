import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
from DataLoader import db_execute_fetch

st.set_page_config(page_title="Tele User Analtics Dashboard", layout="wide")

def loadData():
    query = "select * from TeleInformation"
    df = db_execute_fetch(query, dbName="teledata", rdf=True)
    return df

def selectHandset():
    df = loadData()
    data = st.multiselect("choose Handset Type", list(df['handset_type'].unique()))
    if data:
        df = df[np.isin(df, data).any(axis=1)]
        st.write(df)

def selectHandsetMan():
    df = loadData()
    data = st.multiselect("choose Handset Manfucturer", list(df['handset_manufacturer'].unique()))
    if data:
        df = df[np.isin(df, data).any(axis=1)]
        st.write(df)



st.markdown("# User Analytics")
st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Tweets by Author</p>", unsafe_allow_html=True)
selectHandset()
st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Tweets by PLace</p>", unsafe_allow_html=True)
selectHandsetMan()

