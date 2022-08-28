import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

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
    
    
    st.pyplot(fig)
    
def plot_bar(df:pd.DataFrame, x_col:str, y_col:str, title:str, xlabel:str, ylabel:str)->None:
    fig = plt.figure(figsize=(10, 6))
    plt.bar(df[x_col].head(10), df[y_col].head(10))
    plt.title(title, size=20)
    plt.xticks(rotation=75, fontsize=14)
    plt.yticks( fontsize=14)
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    
    st.pyplot(fig)
    

def showCluster():
    df = loadData()
    # scale / Normalize each engagement metric
    x = df[['session_frequency', 'session_duration', 'total_dl_and_ul_data']].values
    
    scaler = StandardScaler()
    escaled_features = scaler.fit_transform(x)
    escaled_data = pd.DataFrame()
    escaled_data['session_frequency'] = escaled_features[:][:,0]
    escaled_data['session_duration'] = escaled_features[:][:,1]
    escaled_data['total_dl_and_ul_data'] = escaled_features[:][:,2]
    
    ekmeans = KMeans(
       init = "k-means++",
       n_clusters=3,
       n_init=10,
       max_iter=300,
       random_state=0 )
    
    elabel = ekmeans.fit(escaled_data)
    
    # add the labels to Dataframe
    escaled_data['label'] = ekmeans.labels_ 
    
    fig = plt.figure(figsize = (10,8))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(
            escaled_data[escaled_data['label'] == 0]["total_dl_and_ul_data"],
            escaled_data[escaled_data['label'] == 0]["session_frequency"],
            escaled_data[escaled_data['label'] == 0]["session_duration"]
            ,s = 30, c = 'green', label = "More Engaged with High Frequency, data usage and duration")

    ax.scatter(
            escaled_data[escaled_data['label'] == 1]["total_dl_and_ul_data"],
            escaled_data[escaled_data['label'] == 1]["session_frequency"],
            escaled_data[escaled_data['label'] == 1]["session_duration"]
            ,s = 30, c = 'red', label = "Less Engagement with less data and duration")

    ax.scatter(
            escaled_data[escaled_data['label'] == 2]["total_dl_and_ul_data"],
            escaled_data[escaled_data['label'] == 2]["session_frequency"],
            escaled_data[escaled_data['label'] == 2]["session_duration"]
            ,s = 30, c = 'yellow', label = "Medium Engagement with less data and duration")

    # ax.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1], s = 100, c = "yellow", label = "centroids")
    ax.set_xlabel("Total DL and UL Data")
    ax.set_ylabel("Session Frequency")
    ax.set_zlabel("Session Duration")
    ax.legend()
    
    
    st.pyplot(fig)
    
        
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

def showBar(col1, col2, title, name1, name2):
    df = loadData()
    plot_bar(df, col1, col2, title, name1, name2)
    
def showBarSorted(col1, col2, title, name1, name2, top):
    df = loadData()
    
    top_sat = df.sort_values(by =[col2], ascending=False).head(top)
    
    plot_bar(top_sat, col1, col2, title, name1, name2)
    
def compa():

    df = loadData()

    col1, col2 = st.columns(2)

    with col1:
        first = st.selectbox("X Axis the", list(df.columns))
    with col2:
        second = st.selectbox("Y Axis", list(df.columns))

    showBar(first, second, first +" VS "+ second, first, second)



def top10():

    df = loadData()

    col1, col2 = st.columns(2)
    with col1:
        second = st.selectbox("X Axis", list(df.columns))
    with col2:
        top = st.selectbox("Show Top", [3, 5, 10, 20, 30, 40, 50])
    
    
    showBarSorted('MSISDN', second, 'MSISDN vs' + second, 'MSISDN', second, top)

st.markdown("# User Engagement Analysis")


showCluster()

st.markdown("### Top Engagements")
top10()


st.markdown("### Bar Plots")
compa()

selectHandsetMan()
selectHandset()

