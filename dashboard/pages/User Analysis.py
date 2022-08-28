import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from DataLoader import db_execute_fetch

st.set_page_config(page_title="Tele User Analtics Dashboard", layout="wide")

def loadData():
    query = "select * from TeleInformation"
    df = db_execute_fetch(query, dbName="teledata", rdf=True)
    return df

def selectTop10Handset():
    df = loadData()
    fig, axes = plt.subplots(nrows=1, ncols=3, sharey=True, tight_layout=True)
    fig.set_size_inches(12, 6)
    fig.suptitle('The top 5 Handsets per top 3 Handset Manufacturer')

    counter = 0
    for man_name in dict(df['handset_manufacturer'].value_counts()[:3]):
        one = df[df["handset_manufacturer"] == man_name]['handset_type'].value_counts()[:5]
        one.plot(ax = axes[counter], kind='bar')
        axes[counter].set_title(man_name+" Handsets")
        
        counter += 1
    
    st.pyplot(fig)
    
    
def plot_hist(df:pd.DataFrame, column:str, color:str):
    fig = plt.figure(figsize=(15, 10))
    
    sns.displot(data=df, x=column, color=color, kde=True, height=7, aspect=2)
    plt.title(f'Distribution of {column}', size=20, fontweight='bold')
    plt.show()
    
    st.pyplot(fig)
    
def plot_bar(df:pd.DataFrame, x_col:str, y_col:str, title:str, xlabel:str, ylabel:str)->None:
    fig = plt.figure(figsize=(12, 7))
    sns.barplot(data = df, x=x_col, y=y_col)
    plt.title(title, size=20)
    plt.xticks(rotation=75, fontsize=14)
    plt.yticks( fontsize=14)
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    plt.show()
    
    st.pyplot(fig)

def showSessionDist():
    df = loadData()
    plot_hist(df.head(10), "session_duration", "blue")
    
        
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



st.markdown("# User Overview analysis")

selectTop10Handset()
selectHandsetMan()
selectHandset()

